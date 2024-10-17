from functools import wraps

from bebinca.configs import settings
from bebinca.utils.log_util import logger

app_env = settings.env


def log4p(func_name):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if app_env == 'dev':
                log_func = getattr(logger, func_name, None)
                if callable(log_func):  # 对象是否可调用
                    log_func(*args, **kwargs)
            return func(self, *args, **kwargs)
        return wrapper
    return decorator
