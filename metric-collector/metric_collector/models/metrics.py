import pandas as pd
import numpy as np

from prom import Prometheus


class NamespaceMetrics:
    def __init__(self, deploys: list, metrics_names: list) -> None:
        self.__metrics = {}
        for name in metrics_names:
            self.__metrics[name] = pd.DataFrame(columns=deploys, dtype=np.float32)

    def __str__(self) -> str:
        s = ""
        for name in self.__metrics.keys():
            s += f"{name}\n"
            s += self.__metrics[name].to_string()
            s += "\n"
        return s

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
