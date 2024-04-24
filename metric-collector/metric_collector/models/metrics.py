import pandas as pd
from prometheus_api_client import PrometheusConnect


class Metrics:
    def __init__(self, targets=None, prom_url="http://localhost:9090/") -> None:
        self.set_targets(targets)
        self.__queries = [
            [
                "sum(irate(container_cpu_usage_seconds_total{%s}[1m])) by (pod)",
                "cpu",
            ],
        ]
        self.__prom = PrometheusConnect(url=prom_url)

    def __to_pod_label(deploys):
        pods = [f"{deploy}-.*" for deploy in deploys]
        return "|".join(pods)

    def __format_query(query, ns, deploys):
        pods = Metrics.__to_pod_label(deploys)
        return query % f'namespace="{ns}", pod=~"{pods}"'

    def __query_prom(self, query):
        try:
            res = self.__prom.custom_query(query)
            return res
        except Exception as e:
            print("[Error][Collector] Cannot query Prometheus\n", e)
        return {}

    def __match_deploy(pod: str, deploys: list):
        for deploy in deploys:
            if pod.startswith(deploy):
                return deploy
        return None

    def __agg_by_pod(res, deploys, label):
        df = pd.DataFrame(res)

        # set pod name of each row
        df["pod"] = df["metric"].apply(lambda metric: metric["pod"])
        # convert pod name to deploy name
        df["deploy"] = df["pod"].apply(Metrics.__match_deploy, deploys=deploys)
        # extract values (discard timestamp)
        df[label] = df["value"].apply(lambda v: v[1])

        df.drop(columns=["metric", "pod", "value"], inplace=True)
        result = df.groupby("deploy").aggregate({label: "sum"}).reset_index()
        result.set_index("deploy", inplace=True)
        return result

    def __query(self, ns):
        ns_metrics = pd.DataFrame()
        deploys = self.__targets[ns]

        for q, label in self.__queries:
            query = Metrics.__format_query(q, ns, deploys)
            metrics = self.__query_prom(query)
            if len(metrics) == 0:
                continue

            if label == "cpu":
                metrics = Metrics.__agg_by_pod(metrics, deploys, "cpu")
            else:
                # TODO: aggregate by deploy/service
                pass
            ns_metrics[label] = metrics[label]
        return ns_metrics

    def set_targets(self, targets) -> None:
        self.__targets = targets

    def set_prom(self, url):
        self.__prom = PrometheusConnect(url=url)

    def get_all(self) -> dict:
        metrics = {}
        for ns in self.__targets:
            metrics[ns] = self.__query(ns)
        return metrics

    def to_dict(self):
        metrics = self.get_all()
        for ns in metrics:
            metrics[ns] = metrics[ns].to_dict()
        return metrics
