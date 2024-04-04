from ..models.configuration import Configuration
from flask import jsonify
import requests

__COLLECTOR_URL = "http://127.0.0.1:7700"
configuration = Configuration()


def get_config():
    interval = configuration.get_interval()
    targets = configuration.get_targets()
    config = {
        "interval": interval,
        "targets": targets,
    }
    return jsonify(config), 200


def get_interval():
    t = configuration.get_interval()
    interval = {"interval": t}
    return jsonify(interval), 200


def set_interval(t):
    configuration.set_interval(t)

    # Send interval to collector
    url = f"/interval/{t}"
    __send_to_collector(url)

    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def get_targets():
    targets = configuration.get_targets()
    return jsonify(targets), 200


def add_target(ns, name):
    configuration.add_target(ns, name)

    # Send targets to collector
    targets = configuration.get_targets()
    __send_to_collector("/targets", targets)

    msg = {"message": f"{name} in {ns} is added"}
    return jsonify(msg), 200


def delete_target(ns, name):
    configuration.delete_target(ns, name)

    # Send targets to collector
    targets = configuration.get_targets()
    __send_to_collector("/targets", targets)

    msg = {"message": f"{name} in {ns} is deleted"}
    return jsonify(msg), 200


def __send_to_collector(path, json=None):
    url = __COLLECTOR_URL + path
    try:
        if json == None:
            return requests.put(url)
        else:
            return requests.put(url, json=json)
    except:
        # TODO: Exception handling
        print("[Error][API-Server] Cannot send to collector")
