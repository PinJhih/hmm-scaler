from ..models.states import States
from flask import jsonify
import requests
import threading
import time


class Collector:
    def __init__(self) -> None:
        try:
            res = requests.get("http://localhost:7000/config")
            config = res.json()

            self.__interval = config["interval"]
            self.__states = States(config["targets"])

            self.__worker_thread = self.__create_thread()
            self.__worker_thread.start()
        except:
            # TODO: Error handling
            print("[Error][Collector] Cannot get config from API-Server")

    def __get_states(self):
        print("Worker thr start")
        while True:
            time.sleep(self.__interval)
            self.__states.get_all()
            # TODO: Send states to detector

    def __create_thread(self):
        thread = threading.Thread(target=self.__get_states)
        thread.daemon = True
        return thread

    def set_interval(self, t):
        self.__interval = t
        msg = {"message": f"Interval is set to {t}"}
        return jsonify(msg), 200

    def set_targets(self, targets):
        self.__states.set_targets(targets)
        msg = {"message": f"targets are updated"}
        return jsonify(msg), 200
