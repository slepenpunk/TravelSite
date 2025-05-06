import logging
from datetime import datetime, timezone
from functools import wraps

from fastapi import HTTPException
from pythonjsonlogger.json import JsonFormatter

from config import LOG_LEVEL

base_logger = logging.getLogger()
logHandler = logging.StreamHandler()


def handle_and_log_errors(logger: base_logger):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException as e:
                logger.info(f"HTTP exception in {func.__name__}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unknown error in {func.__name__}: {e}")
                raise

        return wrapper

    return decorator


class CustomJsonFormatter(JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname


formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
base_logger.addHandler(logHandler)
base_logger.setLevel(level=LOG_LEVEL)
