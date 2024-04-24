from ..models.metrics import Metrics
from flask import jsonify, current_app
import requests
import threading
import time


class Collector:
    def __init__(self, app) -> None:
        try:
            # Set Flask app context
            self.__app = app
            # Set default values
            self.__interval = 30
            self.__metrics = Metrics({})
            # A thread fetches config. If it fails, it will retry up to 5 times.
            Collector.__create_thread(self.__fetch_config, [5]).start()

            # A thread fetches metrics within a interval
            self.__worker_thread = Collector.__create_thread(
                self.__fetch_metrics, [self.__interval]
            )
            self.__worker_thread.start()
        except Exception as e:
            # TODO: Error handling
            print("[Error][Collector] Cannot create thread.")
            print(e)

    def __fetch_metrics(self, interval):
        elapsed_time = 0
        print(f"[Info][Collector] Worker thread (interval={interval}) started.")
        while True:
            if interval != self.__interval:
                interval = self.__interval
                print(f"[Info][Collector] Worker thread interval is set to {interval}")

            if elapsed_time >= self.__interval:
                metrics = self.__metrics.to_dict()
                try:
                    requests.post("http://localhost:7770/detect", json=metrics)
                except:
                    # TODO: Error handling
                    print(f"[Error][Collector] Cannot send metrics to detector.")
                elapsed_time = 0
            time.sleep(1)
            elapsed_time += 1

    def __fetch_config(self, retry_limit):
        retry_count = 0
        with self.__app.app_context():
            while retry_count < retry_limit:
                try:
                    res = requests.get("http://localhost:7000/config")
                    config = res.json()
                    self.set_interval(config["interval"])
                    self.set_targets(config["targets"])
                    self.set_prom(config["prom"])
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

    def set_interval(self, t):
        self.__interval = t
        msg = {"message": f"Interval is set to {t}"}
        return jsonify(msg), 200

    def set_targets(self, targets):
        self.__metrics.set_targets(targets)
        msg = {"message": f"targets are updated"}
        return jsonify(msg), 200

    def set_prom(self, url):
        self.__metrics.set_prom(url)
        msg = {"message": f"Prom url is set to {url}"}
        return jsonify(msg), 200
