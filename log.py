import logging
import logging.config
from os import getenv

from dotenv import load_dotenv


log = logging.getLogger()

load_dotenv(override=True)

class MuteLogs(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.name in {"werkzeug", "urllib3.connectionpool"}:
            return False
        return True

def setup_logging(default: str = "WARNING"):
    level = getenv("LOG_LEVEL", default)
    config = get_logging_conf(level=level)
    logging.config.dictConfig(config)

def get_logging_conf(level: str) -> dict:
    datefmt: str = "%Y-%m-%dT%H:%M:%S%z"
    return {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": "%(asctime)s %(levelname)s %(name)s %(funcname)s %(thread)d %(message)s",
                "datefmt": datefmt
            }
        },
        "filters": {
            "mute_unwated_logs": {
                "()": "log.MuteLogs"
            }
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "json",
                "stream": "ext://sys.stdout",
                "filters": [
                    "mute_unwated_logs"
                ]
            },
            "file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": level,
                "formatter": "json",
                "filename": "api.log",
                "encoding": "utf8",
                "mode": "a",
                "filters": [
                    "mute_unwated_logs"
                ]
            }
        },
        "root": {
            "handlers": ["stdout", "file_handler"],
            "level": level
        }
    }