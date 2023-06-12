import logging
import re
import string

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


def snake_case_string(s):
    # Remove punctuation
    s = s.translate(str.maketrans("", "", string.punctuation))

    # Lowercase
    s = s.lower()

    # Replace spaces (and possibly multiple spaces) with underscores
    s = re.sub(" +", "_", s)

    return s