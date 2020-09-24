import json
from typing import Optional

import fakeredis
import redis
from django.conf import settings

redis_instance = None

if settings.TEST:
    redis_instance = fakeredis.FakeStrictRedis()
elif settings.REDIS_URL:
    redis_instance = redis.from_url(settings.REDIS_URL, db=0)


def get_cache_key(team_id: int, key: str) -> str:
    return "@c/{}/{}".format(team_id, key)


def get_cached_value(team_id: int, key: str) -> Optional[str]:
    value = redis_instance.get(get_cache_key(team_id, key))
    if value:
        return json.loads(value)


def set_cached_value(team_id: int, key: str, value: str) -> None:
    redis_instance.set(get_cache_key(team_id, key), json.dumps(value))


def clear_cache() -> None:
    if not settings.TEST and not settings.DEBUG:
        raise ("Can only clear redis cache in TEST or DEBUG mode!")

    redis_instance.flushdb()
