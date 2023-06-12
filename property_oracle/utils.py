import logging
import multiprocessing
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# include originating filename in logs
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

NUM_WORKERS = multiprocessing.cpu_count()


def to_snake_case(s):
    # Replace all non-alphanumeric characters with underscores
    s = re.sub(r"\W", "_", s)

    # Split the string into words
    words = s.split()

    return "_".join(re.sub(r"__", "_", word.lower()) for word in words if word != "_")
