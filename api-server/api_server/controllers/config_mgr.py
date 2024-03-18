from ..models import configuration as config_mgr
from flask import jsonify
import requests

__COLLECTOR_URL = "http://127.0.0.1:7700"


def get_config():
    interval = config_mgr.get_interval()
    targets = config_mgr.get_targets()
    config = {
        "interval": interval,
        "targets": targets,
    }
    return jsonify(config), 200


def get_interval():
    t = config_mgr.get_interval()
    interval = {"interval": t}
    return jsonify(interval), 200


def set_interval(t):
    config_mgr.set_interval(t)

    # send update to metric-collector
    url = f"{__COLLECTOR_URL}/interval/{t}"
    res = requests.put(url)
    # TODO: Error handling

    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def get_targets():
    targets = config_mgr.get_targets()
    return jsonify(targets), 200


def add_target(ns, name):
    config_mgr.add_target(ns, name)
    url = f"{__COLLECTOR_URL}/targets"
    targets = config_mgr.get_targets()
    res = requests.put(url, json=targets)
    # TODO: Error handling

    msg = {"message": f"{name} in {ns} is added"}
    return jsonify(msg), 200


def delete_target(ns, name):
    config_mgr.delete_target(ns, name)
    msg = {"message": f"{name} in {ns} is deleted"}
    return jsonify(msg), 200
