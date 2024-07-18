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
        if len(self.__metrics[metrics_name]) == 0:
            self.__metrics[metrics_name] = metrics
        else:
            self.__metrics[metrics_name] = pd.concat(
                [self.__metrics[metrics_name], metrics],
            )
        self.__metrics[metrics_name].reset_index(drop=True, inplace=True)
