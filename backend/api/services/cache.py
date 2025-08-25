import os
import json
import redis

TTL_SECONDS = 180

def get_redis() -> redis.Redis:
    url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    return redis.Redis.from_url(url, decode_responses=True)

def set_status_snapshot(statuses: list[dict]):
    r = get_redis()
    payload = json.dumps(statuses, default=str)
    r.setex("status:lines", TTL_SECONDS, payload)

def get_status_snapshot() -> list[dict]:
    r = get_redis()
    data = r.get("status:lines")
    if not data:
        return []
    parsed = json.loads(data)
    # normalize datetime strings
    for s in parsed:
        if isinstance(s.get("updated_at"), str):
            s["updated_at"] = s["updated_at"]
    return parsed
