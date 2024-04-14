from ..models.states import States

class Detector:
    def detect(self, metric):
        states = States(metric)
