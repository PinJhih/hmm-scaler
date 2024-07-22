import requests
import threading
import time

from flask import Flask

from .models.metrics import Metrics
from .models.prom import Prometheus


class Collector:
    def __init__(self, app: Flask) -> None:
        try:
            # Set Flask app context
            self.__app = app
            # Set default values
            self.__interval = 60
            self.__queries = {
                "cpu": [
                    "sum(irate(container_cpu_usage_seconds_total{%s}[1m])) by (pod) / 16",
                    "pod",
                ]
            }

            # A thread fetches config. If it fails, it will retry up to 5 times.
            Collector.__create_thread(self.__fetch_config, [5]).start()

            # A thread fetches metrics within a interval
            self.__worker_thread = Collector.__create_thread(
                self.__fetch_metrics, [self.__interval]
            )
        except Exception as e:
            # TODO: Error handling
            print(f"[Error][Collector] Cannot create thread.\n\t{e}")

    def __fetch_metrics(self, interval: int):
        elapsed_time = 0
        print(f"[Info][Collector] Worker thread (interval={interval}) started.")
        while True:
            if interval != self.__interval:
                interval = self.__interval
                print(f"[Info][Collector] Worker thread interval is set to {interval}")

            if elapsed_time >= self.__interval:
                # TODO: get metrics and send it to detector
                pass
            time.sleep(1)
            elapsed_time += 1

    def __fetch_config(self, retry_limit: int):
        retry_count = 0
        with self.__app.app_context():
            while retry_count < retry_limit:
                try:
                    res = requests.get("http://localhost:7000/config")
                    config = res.json()

                    # save configurations
                    self.set_interval(config["interval"])
                    self.set_targets(config["targets"])
                    self.set_prom(config["prom"])

                    # init metrics
                    metrics_names = list(self.__queries.keys())
                    self.__metrics = Metrics(self.__targets, metrics_names)

                    self.__worker_thread.start()
                    break
                except:
                    print(
                        "[Error][Collector] Cannot get config from api-server, retry in 5 sec..."
                    )
                time.sleep(5)
                retry_count += 1

        if retry_count == retry_limit:
            print("[Error][Collector] Retry count exceed retry limit!")

    def __create_thread(target, args=()):
        thread = threading.Thread(target=target, args=args)
        thread.daemon = True
        return thread

    def set_interval(self, t: int):
        self.__interval = t

    def set_targets(self, targets: dict):
        self.__targets = targets

    def set_prom(self, url: str):
        self.__prom = Prometheus(url)
