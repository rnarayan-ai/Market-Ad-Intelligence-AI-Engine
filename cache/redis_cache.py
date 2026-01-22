import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

def get_cache(key):
    value = redis_client.get(key)
    return json.loads(value) if value else None

def set_cache(key, value, ttl=3600):
    redis_client.setex(key, ttl, json.dumps(value))
