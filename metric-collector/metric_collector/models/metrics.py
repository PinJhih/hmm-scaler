import pandas as pd
from prometheus_api_client import PrometheusConnect


class Metrics:
    def __init__(
        self,
        targets: dict = {},
        prom_url: str = "http://localhost:9090/",
    ) -> None:
        self.__targets = targets
        self.__queries = [
            [
                "sum(irate(container_cpu_usage_seconds_total{%s}[1m])) by (pod)",
                "cpu",
            ],
            [
                "sum(irate(tcp_read_bytes_total{%s}[1m])) by (deployment)",
                "tcp_read",
            ],
        ]
        self.__prom = PrometheusConnect(url=prom_url)

    def __format_query(query: str, ns: str, deploys: list) -> str:
        pods = [f"{deploy}-.*" for deploy in deploys]
        label = "|".join(pods)
        return query % f'namespace="{ns}", pod=~"{label}"'

    def __query_prom(self, query: str) -> dict:
        try:
            res = self.__prom.custom_query(query)
            return res
        except Exception as e:
            print("[Error][Collector] Cannot query Prometheus\n", e)
        return None

    def __match_deploy(pod: str, deploys: list) -> str:
        for deploy in deploys:
            if pod.startswith(deploy):
                return deploy
        return ""

    def __agg_by_pod(res: dict, deploys: list, label: str) -> pd.DataFrame:
        df = pd.DataFrame(res)

        # set pod name of each row
        df["pod"] = df["metric"].apply(lambda metric: metric["pod"])
        # convert pod name to deploy name
        df["deploy"] = df["pod"].apply(Metrics.__match_deploy, deploys=deploys)
        # extract values (discard timestamp)
        df[label] = pd.to_numeric(df["value"].apply(lambda v: v[1]))
        df.drop(columns=["metric", "pod", "value"], inplace=True)

        result = df.groupby("deploy").aggregate({label: "mean"}).reset_index()
        result.set_index("deploy", inplace=True)
        return result

    def __agg_by_deploy(res: dict, label: str) -> pd.DataFrame:
        df = pd.DataFrame(res)

        # set deploy of row
        df["deploy"] = df["metric"].apply(lambda metric: metric["deployment"])
        # extract values (discard timestamp)
        df[label] = pd.to_numeric(df["value"].apply(lambda v: v[1]))
        df.drop(columns=["metric", "value"], inplace=True)
        df.set_index("deploy", inplace=True)
        return df

    def __get_ns_metrics(self, ns: str) -> pd.DataFrame:
        ns_metrics = pd.DataFrame()
        deploys = self.__targets[ns]

        for q, label in self.__queries:
            query = Metrics.__format_query(q, ns, deploys)
            metrics = self.__query_prom(query)
            if metrics is None:
                continue

            if label == "cpu":
                metrics = Metrics.__agg_by_pod(metrics, deploys, label)
            else:
                metrics = Metrics.__agg_by_deploy(metrics, label)
            ns_metrics[label] = metrics[label]
        return ns_metrics.fillna(0)

    def set_targets(self, targets: dict) -> None:
        self.__targets = targets

    def set_prom(self, url: str) -> None:
        self.__prom = PrometheusConnect(url=url)

    def to_dict(self) -> dict:
        metrics = []
        for ns in self.__targets:
            ns_metrics = self.__get_ns_metrics(ns).reset_index()
            ns_metrics.insert(0, "ns", ns)
            metrics.append(ns_metrics)
        metrics = pd.concat(metrics)

        print(metrics)

        return metrics.to_dict()
