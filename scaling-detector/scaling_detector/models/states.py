import pandas as pd


class States:
    def __init__(self) -> None:
        self.__prev_metrics = dict()
        self.__states = dict()

    def __encode(self, metrics: pd.DataFrame):
        labels = ["cpu"]
        offsets = [-0.4]
        scales = [1]
        step = 0.1

        states = metrics.copy()
        for i in range(len(labels)):
            label = labels[i]
            states[label] -= offsets[i]
            states[label] /= scales[i]
            states[label] //= step
            states[label] = states[label].apply(int)
        return states

    def __add(self, ns: str, metrics: pd.DataFrame):
        diff = metrics.astype("float64") - self.__prev_metrics[ns].astype("float64")
        diff.fillna(0, inplace=True)
        self.__prev_metrics[ns] = metrics

        states = self.__encode(diff)
        if ns not in self.__states:
            self.__states[ns] = dict()

        for deploy in states.index:
            if deploy not in self.__states[ns]:
                self.__states[ns][deploy] = list()

            s = states.loc[deploy, "cpu"]
            self.__states[ns][deploy].append(s)

    def add(self, ns_metrics: dict):
        for ns in ns_metrics:
            deploy_metrics = pd.DataFrame(ns_metrics[ns])

            if ns not in self.__prev_metrics:
                self.__prev_metrics[ns] = deploy_metrics
            else:
                self.__add(ns, deploy_metrics)

    def get(self):
        return self.__states
