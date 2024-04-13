import json
from pathlib import Path


class Configuration:
    __CURRENT_DIR = str(Path(__file__).parent.resolve())
    __CONFIG_FILE_PATH = __CURRENT_DIR + "/config.json"

    def __init__(self) -> None:
        self.__interval = 30
        self.__targets = {}

        # Read from file
        self.__load()

    def __load(self) -> None:
        try:
            with open(Configuration.__CONFIG_FILE_PATH, "r") as file:
                config = json.load(file)
                self.__interval = config["interval"]
                self.__targets = config["targets"]
        except FileNotFoundError:
            self.__save()
        except:
            # TODO: Error handling
            print("[Error][API-Server] Cannot read config file")

    def __save(self) -> None:
        try:
            with open(Configuration.__CONFIG_FILE_PATH, "w") as file:
                config = {"interval": self.__interval, "targets": self.__targets}
                json.dump(config, file, indent=4)
        except:
            # TODO: Error handling
            print("[Error][API-Server] Cannot write to config file")

    def get_interval(self) -> int:
        return self.__interval

    def set_interval(self, t: int) -> None:
        self.__interval = t
        self.__save()

    def get_targets(self) -> dict:
        return self.__targets

    def add_target(self, ns: str, deploy: str) -> bool:
        if ns not in self.__targets.keys():
            self.__targets[ns] = []

        if deploy not in self.__targets[ns]:
            self.__targets[ns].append(deploy)
            self.__save()
            return True
        return False

    def delete_target(self, ns: str, deploy: str) -> bool:
        if ns not in self.__targets:
            return False
        if deploy not in self.__targets[ns]:
            return False

        self.__targets[ns].remove(deploy)
        self.__save()
