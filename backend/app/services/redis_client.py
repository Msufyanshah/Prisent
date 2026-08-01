# backend/app/services/redis_client.py
import time
import redis.asyncio as aioredis
from app.config import settings

class MockRedis:
    _data = {}
    _expiries = {}

    @classmethod
    def _cleanup(cls):
        now = time.time()
        expired = [k for k, t in cls._expiries.items() if t < now]
        for k in expired:
            cls._data.pop(k, None)
            cls._expiries.pop(k, None)

    async def get(self, key: str):
        self._cleanup()
        val = self._data.get(key)
        if val is None:
            return None
        if isinstance(val, str):
            return val.encode("utf-8")
        return str(val).encode("utf-8")

    async def setex(self, key: str, seconds: int, value: str):
        self._cleanup()
        self._data[key] = value
        self._expiries[key] = time.time() + seconds

    async def delete(self, key: str):
        self._cleanup()
        self._data.pop(key, None)
        self._expiries.pop(key, None)

    async def incr(self, key: str) -> int:
        self._cleanup()
        val = self._data.get(key, 0)
        try:
            val = int(val) + 1
        except (ValueError, TypeError):
            val = 1
        self._data[key] = val
        return val

    async def decr(self, key: str) -> int:
        self._cleanup()
        val = self._data.get(key, 0)
        try:
            val = int(val) - 1
        except (ValueError, TypeError):
            val = -1
        self._data[key] = val
        return val

    async def expire(self, key: str, seconds: int):
        self._cleanup()
        if key in self._data:
            self._expiries[key] = time.time() + seconds

    async def aclose(self):
        pass

# Global availability flag
_redis_available = None

async def get_redis():
    global _redis_available
    
    if settings.REDIS_URL == ":memory:":
        return MockRedis()

    if _redis_available is False:
        return MockRedis()

    try:
        r = aioredis.from_url(settings.REDIS_URL, socket_timeout=1.0)
        if _redis_available is None:
            await r.ping()
            _redis_available = True
        return r
    except Exception as e:
        print(f"Warning: Redis connection to {settings.REDIS_URL} failed ({str(e)}). Falling back to in-memory MockRedis.")
        _redis_available = False
        return MockRedis()
