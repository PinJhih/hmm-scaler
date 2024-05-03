import requests

from flask import jsonify

from ..models.configuration import Configuration

__COLLECTOR_URL = "http://127.0.0.1:7700"
configuration = Configuration()


def __send_to_collector(path: str, json: dict | None = None) -> requests.Response:
    url = __COLLECTOR_URL + path
    try:
        if json == None:
            return requests.put(url)
        else:
            return requests.put(url, json=json)
    except:
        # TODO: Exception handling
        print("[Error][API-Server] Cannot send to collector")


def get_config():
    interval = configuration.get_interval()
    targets = configuration.get_targets()
    prom = configuration.get_prom()
    config = {
        "interval": interval,
        "targets": targets,
        "prom": prom,
    }
    return jsonify(config), 200


def get_interval():
    t = configuration.get_interval()
    interval = {"interval": t}
    return jsonify(interval), 200


def set_interval(t: int):
    configuration.set_interval(t)

    # Send interval to collector
    url = f"/interval/{t}"
    __send_to_collector(url)

    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def get_targets():
    targets = configuration.get_targets()
    return jsonify(targets), 200


def add_target(ns: str, name: str):
    configuration.add_target(ns, name)

    # Send targets to collector
    targets = configuration.get_targets()
    __send_to_collector("/targets", targets)

    msg = {"message": f"{name} in {ns} is added"}
    return jsonify(msg), 200


def delete_target(ns: str, name: str):
    configuration.delete_target(ns, name)

    # Send targets to collector
    targets = configuration.get_targets()
    __send_to_collector("/targets", targets)

    msg = {"message": f"{name} in {ns} is deleted"}
    return jsonify(msg), 200


def set_prom(url: str):
    configuration.set_prom(url)
    __send_to_collector("/prom", {"url": url})

    msg = {"message": f"prom url is set to {url}"}
    return jsonify(msg), 200


def get_prom():
    prom = {"url": configuration.get_prom()}
    return jsonify(prom), 200
