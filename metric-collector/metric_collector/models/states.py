from .metrics import Metrics


class States:
    def __init__(self, targets) -> None:
        self.__metrics = Metrics(targets)

    def set_targets(self, targets) -> None:
        self.__metrics = targets

    def get_all(self) -> dict:
        metrics = self.__metrics.get_all()

        # TODO: Convert metrics to states
        print(metrics)
        return {}
