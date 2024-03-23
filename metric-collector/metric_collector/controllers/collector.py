from flask import jsonify
import requests
import threading
import time

__interval = 30
__targets = {}
__thread = None


def __collect_metrics():
    while True:
        # TODO: request to Prometheus
        time.sleep(__interval)
        print(f"collect metrics...")


def __init():
    # TODO: error handling
    res = requests.get("http://localhost:7000/config")
    config = res.json()

    global __interval, __targets
    __interval = config["interval"]
    __targets = config["targets"]

    global __thread
    __thread = threading.Thread(target=__collect_metrics)
    __thread.daemon = True
    __thread.start()


def set_interval(t):
    global __interval
    __interval = t
    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def set_targets(targets):
    global __targets
    __targets = targets
    msg = {"message": f"targets are updated"}
    return jsonify(msg), 200


__init()
