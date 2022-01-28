"""Configs for the library."""

import os
import logging
import logging.config

LIBRARY_NAME = os.path.basename(os.path.dirname(__file__))

# Formats for logging
LOGGING_DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"
NORMAL_LOGGING_FORMAT = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
VERBOSE_LOGGING_FORMAT = (
    "%(asctime)s %(levelname)-8s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
)

# Configurable logging settings
LOGGING_LEVEL = os.environ.get(f"{LIBRARY_NAME.upper()}_LOGGING_LEVEL", logging.DEBUG)
LOG_ALL_THE_THINGS = os.environ.get(f"{LIBRARY_NAME.upper()}_LOG_ALL_THE_THINGS")
LOGGING_FORMATTER = os.environ.get(
    f"{LIBRARY_NAME.upper()}_LOGGING_VERBOSITY", "verbose"
)


ERROR_FILENAME = "error.log"
INFO_FILENAME = "info.log"
_BASE_FOLDER = f".{LIBRARY_NAME}"
_BASE_PATH = os.path.expanduser("~")

LIBRARY_PATH = os.path.join(_BASE_PATH, _BASE_FOLDER)
ERROR_LOG_PATH = os.path.join(LIBRARY_PATH, ERROR_FILENAME)
INFO_LOG_PATH = os.path.join(LIBRARY_PATH, INFO_FILENAME)


if not os.path.exists(LIBRARY_PATH):
    os.makedirs(LIBRARY_PATH)


class ErrorFilter(logging.Filter):
    """Filter class for error only logs."""

    # pylint: disable=too-few-public-methods
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter down to only error level logs."""
        return record.levelno == logging.ERROR


# General logging config here.
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"errorfilter": {"()": ErrorFilter}},
    "formatters": {
        "verbose": {"datefmt": LOGGING_DATE_FORMAT, "format": VERBOSE_LOGGING_FORMAT},
        "normal": {"datefmt": LOGGING_DATE_FORMAT, "format": NORMAL_LOGGING_FORMAT},
    },
    "handlers": {
        "console": {
            "level": LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": LOGGING_FORMATTER,
        },
        "info": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": INFO_LOG_PATH,
            "formatter": LOGGING_FORMATTER,
        },
        "null": {
            "level": LOGGING_LEVEL,
            "class": "logging.NullHandler",
            "formatter": LOGGING_FORMATTER,
        },
        "error": {
            "level": logging.ERROR,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": ERROR_LOG_PATH,
            "filters": ["errorfilter"],
            "formatter": LOGGING_FORMATTER,
        },
    },
    "loggers": {
        LIBRARY_NAME: {"handlers": ["console", "info", "error"], "level": LOGGING_LEVEL}
    },
}

if LOG_ALL_THE_THINGS:
    # This will log everything from all libraries (altering the root logger).  Use when
    # troubleshooting third party libraries rather than your own.
    LOGGING_CONFIG["loggers"] = {
        "": {"handlers": ["console", "info", "error"], "level": 0}
    }


# Configure the logging, and then log a message after import of the library.
logging.config.dictConfig(LOGGING_CONFIG)
LOGGER = logging.getLogger(LIBRARY_NAME)
if LOG_ALL_THE_THINGS:
    LOGGER.warning(
        "Warning!  You've enabled logging at the root logger level.  This may result in a lot of logging!"
    )
LOGGER.info("Loaded %s library with %s log level.", LIBRARY_NAME, LOGGING_LEVEL)
LOGGER.info("Using %s log formatter.", LOGGING_FORMATTER)
