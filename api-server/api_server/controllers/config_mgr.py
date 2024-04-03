from ..models.configuration import Configuration
from flask import jsonify
import requests

__COLLECTOR_URL = "http://127.0.0.1:7700"
config = Configuration()


def get_config():
    interval = config.get_interval()
    targets = config.get_targets()
    config = {
        "interval": interval,
        "targets": targets,
    }
    return jsonify(config), 200


def get_interval():
    t = config.get_interval()
    interval = {"interval": t}
    return jsonify(interval), 200


def set_interval(t):
    config.set_interval(t)

    # Send interval to collector
    url = f"{__COLLECTOR_URL}/interval/{t}"
    res = requests.put(url)
    # TODO: Error handling

    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def get_targets():
    targets = config.get_targets()
    return jsonify(targets), 200


def add_target(ns, name):
    config.add_target(ns, name)

    # Send targets to collector
    url = f"{__COLLECTOR_URL}/targets"
    targets = config.get_targets()
    res = requests.put(url, json=targets)
    # TODO: Error handling

    msg = {"message": f"{name} in {ns} is added"}
    return jsonify(msg), 200


def delete_target(ns, name):
    config.delete_target(ns, name)

    # Send targets to collector
    url = f"{__COLLECTOR_URL}/targets"
    targets = config.get_targets()
    res = requests.put(url, json=targets)

    msg = {"message": f"{name} in {ns} is deleted"}
    return jsonify(msg), 200
