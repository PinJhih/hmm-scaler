import pandas as pd
import numpy as np


class NamespaceMetrics:
    def __init__(self, deploys: list, metrics_names: list) -> None:
        self.__deploys = deploys
        self.__metrics = {}
        for name in metrics_names:
            self.__metrics[name] = pd.DataFrame(columns=deploys, dtype=np.float32)

    def insert(self, metrics_name: str, metrics: pd.DataFrame) -> None:
        m = self.__metrics[metrics_name]
        if len(m) == 0:
            # ensure metrics contains all deploys
            for deploy in m.columns:
                if deploy not in metrics.columns:
                    metrics[deploy] = 0

        m = pd.concat([m, metrics])
        m.reset_index(inplace=True, drop=True)
        m.interpolate(method="linear", inplace=True)
        self.__metrics[metrics_name] = m

    def to_dict(self) -> dict:
        current_metrics = dict()
        for deploy in self.__deploys:
            m = []
            for _, metrics in self.__metrics.items():
                m.append(metrics.iloc[-1][deploy])
            current_metrics[deploy] = tuple(m)
        return current_metrics


class Metrics:
    def __init__(self, targets: dict, metrics_names: list) -> None:
        self.__metrics = dict()
        for ns, deploys in targets.items():
            self.__metrics[ns] = NamespaceMetrics(deploys, metrics_names)

    def insert(self, ns: str, metrics_name: str, metrics: pd.DataFrame):
        self.__metrics[ns].insert(metrics_name, metrics)

    def to_dict(self) -> dict:
        current_metrics = dict()
        for ns, metrics in self.__metrics.items():
            current_metrics[ns] = metrics.to_dict()
        return current_metrics
