import threading
import pickle
from pathlib import Path

import numpy as np
from kubernetes import client, config

from ..models.states import States


class Detector:
    __CURRENT_DIR = str(Path(__file__).parent.resolve())
    __MODEL_PATH = __CURRENT_DIR + "/hmm.pkl"

    def __init__(self) -> None:
        with open(Detector.__MODEL_PATH, "rb") as f:
            self.__model = pickle.load(f)
        self.__states = States()

        config.load_kube_config()
        self.__k8s = client.AppsV1Api()

    def __inference(self, seq: list):
        X = np.array([seq]).reshape((1, len(seq)))
        y = self.__model.predict(X)
        return y[-1]

    def __get_replicas(self, ns: str, deploy: str) -> int | None:
        try:
            deployment = self.__k8s.read_namespaced_deployment(deploy, ns)
            return deployment.spec.replicas
        except Exception as e:
            print(f"[Error][Scaler] getting deployment replicas: {e}")
            return None

    def __scale(self, ns: str, deploy: str, replicas: int) -> None:
        try:
            deployment = self.__k8s.read_namespaced_deployment(deploy, ns)
            deployment.spec.replicas = replicas

            self.__k8s.patch_namespaced_deployment(deploy, ns, deployment)
            return True
        except Exception as e:
            print(f"[Error][Scaler] setting deployment replicas: {e}")
            return False

    def detect(self, ns_metrics: dict):
        self.__states.add(ns_metrics)
        sequences = self.__states.get()

        def detection_logic():
            for ns in sequences:
                for deploy in sequences[ns]:
                    seq = sequences[ns][deploy]
                    print(type(seq))
                    h = self.__inference(seq)

                    if h == 1:
                        print(f"[Info][Scaler] scale UP {deploy} in {ns}")
                        print("\b", seq, h)
                        r = self.__get_replicas(ns, deploy) + 1
                        self.__scale(ns, deploy, r)
                    elif h == 2:
                        print(f"[Info][Scaler] scale DOWN {deploy} in {ns}")
                        r = self.__get_replicas(ns, deploy) - 1
                        print("\b", seq, h)
                        if r != 0:
                            self.__scale(ns, deploy, r)

        detection_thread = threading.Thread(target=detection_logic)
        detection_thread.start()
