import json
from pathlib import Path

__CURRENT_DIR = str(Path(__file__).parent.resolve())
__CONFIG_FILE_PATH = __CURRENT_DIR + "/config.json"

__interval = 30
__targets = {}


def __load_from_file():
    global __interval, __targets
    with open(__CONFIG_FILE_PATH, "r") as file:
        config = json.load(file)
        __interval = config["interval"]
        __targets = config["targets"]


def __save_to_file():
    with open(__CONFIG_FILE_PATH, "w") as file:
        config = {"interval": __interval, "targets": __targets}
        json.dump(config, file, indent=4)


def get_interval():
    return __interval


def set_interval(t):
    global __interval
    __interval = t
    __save_to_file()


def get_targets():
    return __targets


def add_target(ns, name):
    if ns not in __targets.keys():
        __targets[ns] = []

    if name not in __targets[ns]:
        __targets[ns].append(name)
    __save_to_file()


def delete_target(ns, name):
    if (ns in __targets.keys()) and (name in __targets[ns]):
        __targets[ns].remove(name)
    __save_to_file()


__load_from_file()
