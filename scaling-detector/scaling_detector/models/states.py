import pandas as pd
import numpy as np


class States:
    def __init__(self) -> None:
        self.__prev_metrics = pd.DataFrame()
        self.__states = dict()

    def __get_states(self, metrics: pd.DataFrame):
        metrics_diff = metrics.sub(self.__prev_metrics)
        idx = self.__prev_metrics.index

        states = metrics_diff.loc[idx]
        offsets = {"cpu": -0.0627078714735736}
        for col, offset in offsets.items():
            states[col] -= offset

        scales = {"cpu": 0.13807582371262683}
        for col, scale in scales.items():
            states[col] /= scale
            states[col] //= 0.1
        return states

    def add(self, metrics: pd.DataFrame):
        if len(self.__prev_metrics) == 0:
            self.__prev_metrics = metrics
            return

        states = self.__get_states(metrics)
        self.__prev_metrics = metrics
        for index in states.index:
            if index not in self.__states.keys():
                self.__states[index] = list()
            value = states.loc[index]["cpu"]

            try:
                value = int(value)
            except:
                value = self.__states[index][-1]
            self.__states[index].append(value)

    def get(self):
        return self.__states
