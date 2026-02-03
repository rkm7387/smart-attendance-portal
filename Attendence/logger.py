import os
import sys
import logging

# Create logs folder, if not exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def get_logger(name="attendence"):
    """
    Create and return a logger that logs to both console and logs/app.log.
    Prevents duplicate handlers and keeps formatting consistent.
    """
    logger = logging.getLogger(name)

    # if handler already exist, return existing logger
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | "
        "%(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # File Handler
    file_handler = logging.FileHandler(
        os.path.join(LOG_DIR, "app.log"),
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # Register Handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False
    return logger
