from ..models.states import States
from pathlib import Path
import numpy as np
import pickle


class Detector:
    __CURRENT_DIR = str(Path(__file__).parent.resolve())
    __MODEL_PATH = __CURRENT_DIR + "/hmm.pkl"

    def __init__(self) -> None:
        pass
        with open(Detector.__MODEL_PATH, "rb") as f:
            self.__model = pickle.load(f)

    def detect(self, metric):
        labels = ["cpu"]
        scales = [1]
        states = States(metric, labels, scales).get_all()

        print(states)
        for ns in states.keys():
            for deploy in states[ns].keys():
                s = states[ns][deploy]
                self.__inference(f"{ns} {deploy}", s)

    def __inference(self, label, state):
        X = np.array(state).reshape([1, 1])
        y = self.__model.predict(X)
        print(label, y)
