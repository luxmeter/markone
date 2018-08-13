import logging
from functools import wraps


def log_api():
    def deco_log(f):
        @wraps(f)
        def f_log(*args, **kwargs):
            log = logging.getLogger(f.__module__)
            log.info(f'Received request on /{f.__name__}')
            result = f(*args, **kwargs)
            return result

        return f_log

    return deco_log
