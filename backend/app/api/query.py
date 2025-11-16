from fastapi import APIRouter, Depends
from app.schemas.query import QueryRequest, QueryResponse
from app.services.agent_service import AgentService
from app.services.redis_service import RedisService

router = APIRouter()


def get_redis_service():
    from app.main import app

    return app.state.redis


@router.post("/query", response_model=QueryResponse)
async def query(req: QueryRequest, redis: RedisService = Depends(get_redis_service)):
    """Handle user query and orchestrate analysis"""
    agent = AgentService(redis)
    result = await agent.handle_query(req.session_id, req.query, req.dataset_id)
    return QueryResponse(**result)
