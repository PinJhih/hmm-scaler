import threading
import pickle
import requests
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from kubernetes import client, config

from ..models.states import States

logger = logging.getLogger("logger1")
file_handler = logging.FileHandler("scaler.log")
file_handler.setFormatter(
    logging.Formatter("\n%(asctime)s [%(levelname)s]\n%(message)s")
)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


class Detector:
    __CURRENT_DIR = str(Path(__file__).parent.resolve())
    __MODEL_PATH = __CURRENT_DIR + "/hmm.pkl"

    def __init__(self) -> None:
        with open(Detector.__MODEL_PATH, "rb") as model:
            self.__model = pickle.load(model)
        self.__states = States()

        config.load_kube_config()
        self.__k8s = client.AppsV1Api()

    def __inference(self, seq: list):
        try:
            X = np.array([seq]).reshape((1, len(seq)))
            y = self.__model.predict(X)
        except:
            print(f"Error: Seq = {seq}")
            y = []
        return y

    def __get_replicas(self, ns: str, deploy: str) -> int | None:
        try:
            deployment = self.__k8s.read_namespaced_deployment(deploy, ns)
            return deployment.spec.replicas
        except Exception as e:
            print(f"[Error][Scaler] getting deployment replicas: {e}")
            return None

    def __get_target_replicas(self, ns: str, deploy: str, response_time: float):
        scale = max(1, round(response_time / 5))
        current_replicas = self.__get_replicas(ns, deploy)

        print(
            f"scale {scale}, curr {current_replicas}, target {int(current_replicas * int(scale))}"
        )
        return int(current_replicas * int(scale))

    def __scale_up(self, ns: str, deploy: str, response_time: float) -> None:
        try:
            before = self.__get_replicas(ns, deploy)
            replicas = self.__get_target_replicas(ns, deploy, response_time)
            deployment = self.__k8s.read_namespaced_deployment(deploy, ns)
            deployment.spec.replicas = replicas

            if replicas > before:
                print(
                    f'[Info][Scaler] Scale "{deploy}" in "{ns}" UP, {before}=> {replicas}'
                )
                self.__k8s.patch_namespaced_deployment(deploy, ns, deployment)

            return True
        except Exception as e:



            print(f"[Error][Scaler] setting deployment replicas: {e}")
            return False

    def __scale_down(self, ns: str, deploy: str) -> None:
        try:
            before = self.__get_replicas(ns, deploy)
            replicas = before - 1
            if replicas <= 0:
                return False

            deployment = self.__k8s.read_namespaced_deployment(deploy, ns)
            deployment.spec.replicas = replicas
            self.__k8s.patch_namespaced_deployment(deploy, ns, deployment)

            if before != replicas:
                print(
                    f'[Info][Scaler] Scale "{deploy}" in "{ns}" Down, {before}=> {replicas}'
                )

            return True
        except Exception as e:
            print(f"[Error][Scaler] setting deployment replicas: {e}")
            return False

    def detect(self, metrics: dict, response_time: float):
        def detection_logic():
            print(f"current response time {response_time}")

            self.__states.add(metrics)
            sequences = self.__states.get()

            logger.info(
                f"curr response time {response_time}\n\n{metrics}\n\n{pd.DataFrame(sequences).transpose()}\n"
            )

            for (ns, deploy), seq in sequences.items():
                hidden_states = self.__inference(seq)
                if len(hidden_states) == 0:
                    continue

                if hidden_states[-1] == 1:
                    self.__scale_up(ns, deploy, response_time)
                elif hidden_states[-1] == 2:
                    self.__scale_down(ns, deploy)

        detection_thread = threading.Thread(target=detection_logic, daemon=True)
        detection_thread.start()
