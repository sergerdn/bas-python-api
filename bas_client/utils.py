import inspect
import logging
import time
from decimal import Decimal

from bas_client.typing import LoggerLike

default_logger = logging.getLogger("utils")


def _get_logger_from_class() -> LoggerLike:
    stack = inspect.stack()
    try:
        return getattr(stack[2][0].f_locals["self"], "logger")
    except AttributeError:
        return default_logger


def time_it(fn):
    """Decorator that reports the execution time."""

    def wrap(*args, **kwargs):
        start = time.time()
        result = fn(*args, **kwargs)
        end = time.time()
        diff = Decimal(end) - Decimal(start)
        class_fn = "{}.{}".format(fn.__module__, fn.__qualname__)
        logger = _get_logger_from_class()
        logger.debug("timeit: {}, {}".format(class_fn, diff))

        return result

    return wrap
