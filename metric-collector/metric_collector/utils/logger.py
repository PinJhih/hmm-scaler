import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [Collector][%(module)s][%(levelname)s] - %(message)s",
)

logger = logging.getLogger(__name__)
