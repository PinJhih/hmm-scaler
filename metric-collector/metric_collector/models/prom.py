import pandas as pd
from prometheus_api_client import PrometheusConnect


class Prometheus:
    def __init__(self, url: str) -> None:
        self.__conn = PrometheusConnect(url=url)

    def __query(self, query: str) -> dict:
        try:
            res = self.__conn.custom_query(query)
            return res
        except Exception as e:
            print(f'[Error][Collector] Error executing query:\n  "{query}"\n{e}')
        return None

    def __match_deploy(pod: str, deploys: list) -> str:
        for deploy in deploys:
            if pod.startswith(deploy):
                return deploy
        return ""

    def __agg_by_pod(res: dict, deploys: list) -> pd.DataFrame:
        df = pd.DataFrame(res)

        # get deploy name of metrics
        df["pod"] = df["metric"].apply(lambda metric: metric["pod"])
        df["deploy"] = df["pod"].apply(Prometheus.__match_deploy, deploys=deploys)

        # extract values (discard timestamp)
        df["value"] = pd.to_numeric(df["value"].apply(lambda v: v[1]))
        df.drop(columns=["metric", "pod"], inplace=True)

        # get average of each deploy
        result = df.groupby("deploy").aggregate({"value": "mean"}).reset_index()
        result.set_index("deploy", inplace=True)
        return result

    def __agg_by_deploy(res: dict) -> pd.DataFrame:
        df = pd.DataFrame(res)

        # set deploy of row
        df["deploy"] = df["metric"].apply(lambda metric: metric["deployment"])

        # extract values (discard timestamp)
        df["value"] = pd.to_numeric(df["value"].apply(lambda v: v[1]))
        df.drop(columns=["metric"], inplace=True)
        df.set_index("deploy", inplace=True)
        return df

    def query_by_pod(self, query: str, ns: str, deploys: list):
        pods = [f"{deploy}-.*" for deploy in deploys]
        label = "|".join(pods)
        query = query % f'namespace="{ns}", pod=~"{label}"'

        res = self.__query(query)
        return Prometheus.__agg_by_pod(res, deploys)

    def query_by_deploy(self, query: str, ns: str, deploy: list):
        label = "|".join(deploy)
        query = query % f'namespace="{ns}", deployment=~"{label}"'

        res = self.__query(query)
        return Prometheus.__agg_by_deploy(res)
