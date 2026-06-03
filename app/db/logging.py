import logging
import sys


def add_sqlalchemy_logging():
    logger = logging.getLogger("sqlalchemy.engine")
    logger.propagate = False
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("\033[35m%(asctime)s [SQLAlchemy] %(message)s\033[39m")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
