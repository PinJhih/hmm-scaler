from flask import jsonify
import json

# TODO: get config from api-server
__interval = 30
__targets = {}


def set_interval(t):
    global __interval
    __interval = t
    msg = {"message": f"interval is set to {t}"}
    return jsonify(msg), 200


def set_targets(targets):
    global __targets

    for target in targets:
        ns = target["namespace"]
        names = target["names"]
        __targets[ns] = names
    
    msg = {"message": f"targets are updated"}
    return jsonify(msg), 200
