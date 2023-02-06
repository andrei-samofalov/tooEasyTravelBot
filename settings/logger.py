import logging.config
import sys


def set_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s %(module)s %(levelname)s] %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )
    return logging.getLogger(name)


setup = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "base": {
            "format": "[%(asctime)s %(module)s %(levelname)s] %(message)s",
            "datefmt": '%d-%m-%Y %H:%M:%S'
        },
        "extended": {
            "format": "%(asctime)s %(levelname)s | %(module)s [line %(lineno)s]: %(message)s",
            "datefmt": '%d-%m-%Y %H:%M:%S'
        },
    },
    "handlers": {
        "screen": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "stream": sys.stdout
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when": "midnight",
            "backupCount": 5,
            "formatter": "extended",
            "level": "DEBUG",
            "filename": "./settings/logs/tooEasyLog.log"
        }
    },
    "loggers": {
        "travelBotLogger": {
            "level": "DEBUG",
            "handlers": ["screen", "file"],
         }
    },
}

logging.config.dictConfig(setup)
logger = logging.getLogger('travelBotLogger')
