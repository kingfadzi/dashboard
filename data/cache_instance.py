from flask_caching import Cache
import redis

# Default to using Redis, but gracefully handle failures
cache_config = {
    "CACHE_TYPE": "redis",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_REDIS_URL": "redis://localhost:6379/0",
}

try:
    redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, socket_timeout=1)
    redis_client.ping()
    print("✅ Redis is running. Caching enabled.")
except redis.ConnectionError:
    print("⚠️ Redis is down. Caching may be unavailable.")
    cache_config["CACHE_TYPE"] = "null"  # Disable caching without modifying app logic

cache = Cache(config=cache_config)