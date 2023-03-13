

import json

from tendril.config import PLATFORM_CACHING_PROVIDER

from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)


if PLATFORM_CACHING_PROVIDER == 'redis':
    logger.info("Using Redis for the platform level cache.")
    import redis
    from tendril.config import REDIS_HOST
    from tendril.config import REDIS_PORT
    from tendril.config import REDIS_DB
    from tendril.config import REDIS_PASSWORD
else:
    raise Exception("A valid PLATFORM_CACHING_PROVIDER is not configured "
                    "and a fallback is not presently implemented.")


redis_connection: redis.Redis = None


def _create_redis_connection():
    global redis_connection
    logger.info("Using Redis server at {}:{}:{} for transit caching"
                "".format(REDIS_HOST, REDIS_PORT, REDIS_DB))
    redis_connection = redis.Redis(host=REDIS_HOST,
                                   port=REDIS_PORT,
                                   db=REDIS_DB,
                                   password=REDIS_PASSWORD)


def _common(namespace=None, key=None):
    if not redis_connection:
        _create_redis_connection()

    if not key:
        raise NotImplementedError(
            "Redis transit caching requires a literal "
            "key to be provided."
        )

    if not namespace:
        logger.warn(f"No transit caching namespace was provided for "
                    f"key {key}. Using 'transit' instead.")

    cache_key = "{}:{}".format(namespace, key)
    return cache_key


def write(value=None, namespace=None, ttl=None, key=None, ser=json.dumps):
    cache_key = _common(namespace=namespace, key=key)
    logger.debug(f"Writing {value} to {cache_key}")
    redis_connection.set(cache_key, ser(value), ex=ttl)


def read(namespace=None, key=None, deser=json.loads):
    cache_key = _common(namespace=namespace, key=key)
    cached_value = redis_connection.get(cache_key)
    logger.debug(f"Read {cached_value} from {cache_key}")
    if cached_value:
        return deser(cached_value)
    else:
        return None


def delete(namespace=None, key=None):
    cache_key = _common(namespace=namespace, key=key)
    redis_connection.delete(cache_key)
