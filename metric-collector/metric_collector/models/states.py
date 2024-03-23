__targets = {}


def __get_metrics():
    # TODO: get metrics from Prometheus
    print(f"collect metrics...")


def get_states():
    __get_metrics()
    # TODO: convert metrics to states
    return {}


def set_targets(target):
    global __targets
    __targets = target
