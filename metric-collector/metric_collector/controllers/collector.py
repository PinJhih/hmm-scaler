from ..models.metrics import Metrics
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
            self.__metrics = Metrics(config["targets"])

            self.__worker_thread = self.__create_thread()
            self.__worker_thread.start()
        except:
            # TODO: Error handling
            print("[Error][Collector] Cannot get config from API-Server")

    def __fetch_metrics(self, interval):
        print(f"[Info][Collector] Worker thread (interval={interval} sec) started.")

        elapsed_time = 0
        while self.__interval == interval:
            time.sleep(1)
            elapsed_time += 1
            if elapsed_time == interval and interval == self.__interval:
                metrics = self.__metrics.get_all()
                try:
                    requests.post("http://localhost:7770/detect", json=metrics)
                except:
                    # TODO: Error handling
                    print(f"[Error][Collector] Cannot send metrics to detector.")

                elapsed_time = 0
        print(f"[Info][Collector] Worker thread (interval={interval} sec) killed.")

    def __create_thread(self):
        interval = self.__interval
        thread = threading.Thread(target=self.__fetch_metrics, args=[interval])
        thread.daemon = True
        return thread

    def set_interval(self, t):
        self.__interval = t
        self.__worker_thread = self.__create_thread()
        self.__worker_thread.start()
        msg = {"message": f"Interval is set to {t}"}
        return jsonify(msg), 200

    def set_targets(self, targets):
        self.__metrics.set_targets(targets)
        msg = {"message": f"targets are updated"}
        return jsonify(msg), 200
