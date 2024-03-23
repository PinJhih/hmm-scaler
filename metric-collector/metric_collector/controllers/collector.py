from ..models import states
from flask import jsonify
import requests
import threading
import time

__interval = 30
__thread = None


def __get_states():
    while True:
        time.sleep(__interval)
        s = states.get_states()
        url = "http://localhost:7770/detect"
        requests.post(url, json=s) # TODO: error handling


def __init():
    # TODO: error handling
    res = requests.get("http://localhost:7000/config")
    config = res.json()

    global __interval, __targets
    __interval = config["interval"]
    __targets = config["targets"]

    global __thread
    __thread = threading.Thread(target=__get_states)
    __thread.daemon = True
    __thread.start()


def set_interval(t):
    global __interval
    __interval = t
    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def set_targets(targets):
    states.set_targets(targets)
    msg = {"message": f"targets are updated"}
    return jsonify(msg), 200


__init()
