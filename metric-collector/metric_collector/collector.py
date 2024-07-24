import requests
import threading
import time

from flask import Flask

from .models.metrics import Metrics
from .utils.prom import Prometheus
from .utils.logger import logger


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

            # TODO: Make SLO configurable
            self.__slo = {"socialnetwork": "nginx-thrift"}

            # A thread fetches config. If it fails, it will retry up to 5 times.
            Collector.__create_thread(self.__fetch_config, [5]).start()

            # A thread fetches metrics within a interval
            self.__worker_thread = Collector.__create_thread(
                self.__detect, [self.__interval]
            )
        except Exception as e:
            # TODO: Error handling
            logger.error(f"Cannot create thread.\n\t{e}")

    def __fetch_metrics(self):
        for ns, deploys in self.__targets.items():
            for name, q in self.__queries.items():
                query, type = q
                if type == "pod":
                    m = self.__prom.query_by_pod(query, ns, deploys)
                else:
                    m = self.__prom.query_by_deploy(query, ns, deploys)
                self.__metrics.insert(ns, name, m)

    def __fetch_slo(self):
        query_latency = "sum(irate(response_latency_ms_sum{%s} [1m])) by (deployment)"
        query_res_count = "sum(irate(response_total{%s} [1m])) by (deployment)"

        slo = {}
        for ns, deploy in self.__slo.items():
            try:
                total_latency = self.__prom.query_by_deploy(query_latency, ns, [deploy])
                total_response = self.__prom.query_by_deploy(
                    query_res_count, ns, [deploy]
                )
                avg_latency = (total_latency / total_response).values.flatten()[0]
            except:
                # TODO: missing value handling
                avg_latency = 5
            slo[ns] = avg_latency
        return slo

    def __detect(self, interval: int):
        elapsed_time = 0
        logger.info(f"Worker thread (interval={interval}) started")
        while True:
            if interval != self.__interval:
                interval = self.__interval
                logger.info(f"Worker thread interval is set to {interval}")

            if elapsed_time >= self.__interval:
                elapsed_time = 0
                self.__fetch_metrics()
                metrics = self.__metrics.to_dict()
                slo = self.__fetch_slo()

                data = {"metrics": metrics, "slo": slo}
                requests.post("http://localhost:7770/detect", json=data)
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
                    logger.warn("Cannot get config from api-server, retry in 5 sec...")
                time.sleep(5)
                retry_count += 1

        if retry_count == retry_limit:
            logger.error("Retry count exceed retry limit!")

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
