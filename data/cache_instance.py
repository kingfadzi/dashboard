from flask_caching import Cache
import redis
import os
from urllib.parse import urlparse

cache_config = {
    "CACHE_TYPE": os.environ.get("CACHE_TYPE", "null"),
    "CACHE_DEFAULT_TIMEOUT": int(os.environ.get("CACHE_DEFAULT_TIMEOUT", 300)),
    "CACHE_REDIS_URL": os.environ.get("CACHE_REDIS_URL", "redis://localhost:6379/0"),
}

# Parse Redis connection info
parsed = urlparse(cache_config["CACHE_REDIS_URL"])
host = parsed.hostname or "localhost"
port = parsed.port or 6379
db = int(parsed.path.lstrip("/") or 0)

print(f"ℹ️ Connecting to Redis at {host}:{port}, DB {db}")

try:
    redis_client = redis.StrictRedis(host=host, port=port, db=db, socket_timeout=1)
    redis_client.ping()
    print("✅ Redis is running. Caching enabled.")
except redis.ConnectionError:
    print("⚠️ Redis is down. Caching may be unavailable.")
    cache_config["CACHE_TYPE"] = "null"

cache = Cache(config=cache_config)
