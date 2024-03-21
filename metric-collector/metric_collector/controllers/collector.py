from flask import jsonify
import requests
import threading
import time

__interval = 30
__targets = {}
__thread = None


def __set_targets(data):
    global __targets
    for target in data:
        ns = target["namespace"]
        names = target["names"]
        __targets[ns] = names


def __collect_metrics():
    while True:
        # TODO: request to Prometheus
        print("collect metrics...")
        time.sleep(__interval)


def __init():
    # TODO: error handling
    res = requests.get("http://localhost:7000/config")
    config = res.json()

    global __interval
    __interval = config["interval"]
    __set_targets(config["targets"])

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
    __set_targets(targets)
    msg = {"message": f"targets are updated"}
    return jsonify(msg), 200


__init()
