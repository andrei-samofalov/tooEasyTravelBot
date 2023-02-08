from functools import wraps

from settings import logger


def deprecated(func: callable) -> callable:
    @wraps(func)
    def function(*args, **kwargs):
        logger.warning(f'This function "({func.__name__})" is deprecated. Please, use actual version')
        return func(*args, **kwargs)

    return function
