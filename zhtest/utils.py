from django.core.cache import cache
from zhtest.settings import CACHE_VIEW_KEY_PREFIX


def delete_cache(key_prefix: str):
    """
    Delete all cache keys with the given prefix.
    """  
    redis_client = cache.client.get_client()
    cache_keys = redis_client.keys(f":1:views.decorators.cache.cache_page.{key_prefix}*")
    for key in cache_keys:
        redis_client.delete(key)
