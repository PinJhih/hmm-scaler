from ..models.states import States


class Detector:
    def detect(self, metric):
        labels = ["cpu"]
        scales = [1]
        states = States(metric, labels, scales)

        print(states.get_all())
