from flask import jsonify
import requests

__interval = 30
__targets = {}


def __set_targets(data):
    global __targets
    for target in data:
        ns = target["namespace"]
        names = target["names"]
        __targets[ns] = names


def __init():
    # TODO: error handling
    res = requests.get("http://localhost:7000/config")
    config = res.json()

    global __interval
    __interval = config["interval"]
    __set_targets(config["targets"])


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
