from pydantic import BaseModel
from typing import Optional, Dict, Any, List


class QueryRequest(BaseModel):
    session_id: str
    query: str
    dataset_id: Optional[str] = None


class QueryResponse(BaseModel):
    job_id: str
    status: str
    plan: Optional[str] = None
    code: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    artifacts: Optional[List[str]] = None
    explanation: Optional[str] = None
    error: Optional[str] = None


class SessionCreate(BaseModel):
    user_id: Optional[str] = None


class SessionResponse(BaseModel):
    session_id: str
    created_at: str
    last_activity: str
