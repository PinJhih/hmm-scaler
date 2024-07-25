import pandas as pd
import numpy as np


class NamespaceMetrics:
    def __init__(self, deploys: list, metrics_names: list) -> None:
        self.__deploys = deploys
        self.__metrics = dict()
        for name in metrics_names:
            self.__metrics[name] = pd.DataFrame(columns=deploys, dtype=np.float32)

        self.__slo = pd.DataFrame(columns=["slo"], dtype=np.float32)

    def insert(self, metrics_name: str, metrics: pd.DataFrame) -> None:
        m = self.__metrics[metrics_name]
        if len(m) == 0:
            # ensure metrics contains all deploys
            for deploy in m.columns:
                if deploy not in metrics.columns:
                    # TODO: missing value handling
                    metrics[deploy] = 0

        m = pd.concat([m, metrics])
        m.reset_index(inplace=True, drop=True)
        m.interpolate(method="linear", inplace=True)
        self.__metrics[metrics_name] = m

    def insert_slo(self, latency: float):
        slo = self.__slo
        if latency == np.nan and len(self.__slo) == 0:
            # TODO: missing value handling
            latency = 5
        current_slo = pd.DataFrame({"slo": [latency]})
        slo = pd.concat([slo, current_slo])
        slo.reset_index(inplace=True, drop=True)
        slo.interpolate(method="linear", inplace=True)
        self.__slo = slo

    def to_dict(self) -> dict:
        current_metrics = dict()
        for deploy in self.__deploys:
            m = []
            for _, metrics in self.__metrics.items():
                if len(metrics) == 0:
                    continue
                m.append(metrics.iloc[-1][deploy])
            current_metrics[deploy] = m
        current_slo = self.__slo.iloc[-1]["slo"]
        return {"metric": current_metrics, "slo": current_slo}


class Metrics:
    def __init__(self, targets: dict, metrics_names: list) -> None:
        self.__metrics = dict()
        for ns, deploys in targets.items():
            self.__metrics[ns] = NamespaceMetrics(deploys, metrics_names)

    def insert(self, ns: str, metrics_name: str, metrics: pd.DataFrame):
        self.__metrics[ns].insert(metrics_name, metrics)

    def insert_slo(self, ns: str, slo: float):
        self.__metrics[ns].insert_slo(slo)

    def to_dict(self) -> dict:
        current_metrics = dict()
        for ns, metrics in self.__metrics.items():
            current_metrics[ns] = metrics.to_dict()
        return current_metrics
