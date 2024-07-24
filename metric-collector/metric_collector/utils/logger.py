import logging

logger = logging.getLogger("collector-logger")
logger.setLevel(logging.DEBUG)

# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# set formatter
formatter = logging.Formatter(
    "%(asctime)s [Collector][%(module)s][%(levelname)s] - %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)
