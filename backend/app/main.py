from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api import query, datasets, sessions, langchain_query, enhanced_query
from app.services.redis_service import RedisService
from app.utils.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Data Science Research Assistant Agent")
    
    # Initialize Redis
    redis_service = RedisService()
    await redis_service.connect()
    app.state.redis = redis_service
    
    # Initialize Database
    from app.db.database import init_db
    init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    await redis_service.close()
    logger.info("Shutting down")

app = FastAPI(
    title="DS Research Agent API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api/v1", tags=["query"])
app.include_router(langchain_query.router, prefix="/api/v1", tags=["langchain"])
app.include_router(datasets.router, prefix="/api/v1", tags=["datasets"])
app.include_router(sessions.router, prefix="/api/v1", tags=["sessions"])
app.include_router(enhanced_query.router, prefix="/api/v1", tags=["enhanced"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    return {
        "message": "Data Science Research Assistant Agent API",
        "docs": "/docs"
    }
