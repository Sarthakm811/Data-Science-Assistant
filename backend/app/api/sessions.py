from fastapi import APIRouter, Depends
from datetime import datetime
import uuid
from app.schemas.query import SessionCreate, SessionResponse
from app.services.redis_service import RedisService

router = APIRouter()


def get_redis_service():
    from app.main import app

    return app.state.redis


@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    req: SessionCreate, redis: RedisService = Depends(get_redis_service)
):
    """Create a new session"""
    session_id = str(uuid.uuid4())
    now = datetime.utcnow().isoformat()

    session_data = {
        "session_id": session_id,
        "user_id": req.user_id,
        "created_at": now,
        "last_activity": now,
    }

    await redis.set_session(session_id, session_data)

    return SessionResponse(session_id=session_id, created_at=now, last_activity=now)


@router.get("/sessions/{session_id}/history")
async def get_session_history(
    session_id: str, redis: RedisService = Depends(get_redis_service)
):
    """Get session history"""
    history = await redis.get_history(session_id)
    return {"history": history}
