

from functools import wraps


def cache(namespace=None, ttl=None, key=None):
    def _wrapper_factory(func):
        @wraps(func)
        def wrapper_func(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper_func
    return _wrapper_factory
