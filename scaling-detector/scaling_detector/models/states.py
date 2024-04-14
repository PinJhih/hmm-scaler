class States:
    def __init__(self, metrics, labels, scales) -> None:
        self.__states = dict()
        for ns in metrics.keys():
            self.__states[ns] = States.__mapping(metrics[ns], labels, scales)

    def get_all(self) -> dict:
        return self.__states

    def __mapping(metrics, labels, scale):
        states = dict()
        for deploy in metrics.keys():
            state = []
            for i in range(len(labels)):
                label = labels[i]
                metric = metrics[deploy][label] / scale[i]
                if metric == 0:
                    s = 0
                else:
                    s = int(metric // 0.1) + 1
                state.append(s)
            states[deploy] = state
        return states
