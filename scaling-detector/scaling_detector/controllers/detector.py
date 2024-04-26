from ..models.states import States
from pathlib import Path
import numpy as np
import pickle


class Detector:
    __CURRENT_DIR = str(Path(__file__).parent.resolve())
    __MODEL_PATH = __CURRENT_DIR + "/hmm.pkl"

    def __init__(self) -> None:
        with open(Detector.__MODEL_PATH, "rb") as f:
            self.__model = pickle.load(f)
        self.__states = States()

    def __inference(self, seq):
        X = np.array([seq]).reshape((1, len(seq)))
        y = self.__model.predict(X)
        return y[-1]

    def detect(self, ns_metrics):
        self.__states.add(ns_metrics)
        sequences = self.__states.get()
        
        print(f"[detector] prediction")
        for ns in sequences:
            for deploy in sequences[ns]:
                seq = sequences[ns][deploy]
                h = self.__inference(seq)

                # TODO: Scaling by k8s API
                print(f"[detector] {ns}/{deploy}")
                print(f"[detector] {seq} => {h}")
