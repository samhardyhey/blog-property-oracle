import logging
import re

logger = logging.getLogger()
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)


def to_snake_case(s):
    """
    Converts a string to snake case.
    """
    # Replace all non-alphanumeric characters with underscores
    s = re.sub(r"\W", "_", s)

    # Split the string into words
    words = s.split()

    return "_".join(re.sub(r"__", "_", word.lower()) for word in words if word != "_")
