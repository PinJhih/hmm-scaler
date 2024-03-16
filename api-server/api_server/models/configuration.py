# TODO: read from file and DB
__interval = 30
__targets = {
    "social-network": [
        "compose-post-service",
        "home-timeline-redis",
        "home-timeline-service",
    ]
}


def get_interval():
    return __interval


def set_interval(t):
    global __interval
    __interval = t
    # TODO: write to file


def get_targets():
    targets = []
    for ns, names in __targets.items():
        target = {"namespace": ns, "names": list(names)}
        targets.append(target)
    return targets


def add_target(ns, name):
    if ns not in __targets.keys():
        __targets[ns] = set()
    __targets[ns].add(name)
    # TODO: add to DB


def delete_target(ns, name):
    if (ns in __targets.keys()) and (name in __targets[ns]):
        __targets[ns].remove(name)
    # TODO: delete from DB
