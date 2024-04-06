class States:
    def __init__(self, targets) -> None:
        self.__targets = targets

    def set_targets(self, targets) -> None:
        self.__targets = targets

    def get_all(self) -> dict:
        # TODO: maps to states
        self.__get_metrics()
        print("Get states...")

    def __get_metrics(self):
        # TODO: query Prometheus
        print("Query Prom...")
