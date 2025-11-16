import redis.asyncio as redis
import json
from typing import Optional, Dict, Any
from app.utils.config import settings


class RedisService:
    def __init__(self):
        self.client: Optional[redis.Redis] = None

    async def connect(self):
        self.client = await redis.from_url(
            settings.redis_url, encoding="utf-8", decode_responses=True
        )

    async def close(self):
        if self.client:
            await self.client.close()

    async def set_session(self, session_id: str, data: Dict[str, Any], ttl: int = 3600):
        """Store session data with TTL"""
        await self.client.setex(f"session:{session_id}", ttl, json.dumps(data))

    async def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data"""
        data = await self.client.get(f"session:{session_id}")
        return json.loads(data) if data else None

    async def append_to_history(self, session_id: str, message: Dict[str, Any]):
        """Append message to session history"""
        await self.client.rpush(f"history:{session_id}", json.dumps(message))
        await self.client.expire(f"history:{session_id}", 3600)

    async def get_history(self, session_id: str, limit: int = 10) -> list:
        """Get recent session history"""
        messages = await self.client.lrange(f"history:{session_id}", -limit, -1)
        return [json.loads(msg) for msg in messages]
