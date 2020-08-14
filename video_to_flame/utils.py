from functools import wraps
import time

from util.log_conf import get_logger
logger = get_logger(__file__)


def stop_watch(func):
    @ wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        proc_time = time.time() - start
        logger.info(f"{func.__name__} : {proc_time} sec")
        return result
    return wrapper
