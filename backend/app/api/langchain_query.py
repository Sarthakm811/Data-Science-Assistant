"""
LangChain-powered query endpoint
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time

from app.schemas.query import QueryRequest, QueryResponse
from app.services.langchain_agent import LangChainAgent
from app.db.database import get_db
from app.db.repository import QueryRepository

router = APIRouter()

@router.post("/query/langchain", response_model=QueryResponse)
async def query_with_langchain(
    req: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Handle query using LangChain orchestration
    This provides more sophisticated multi-tool reasoning
    """
    start_time = time.time()
    
    # Create query record
    query_record = QueryRepository.create_query(
        db=db,
        session_id=req.session_id,
        query_text=req.query,
        dataset_id=req.dataset_id
    )
    
    try:
        # Initialize LangChain agent
        agent = LangChainAgent()
        
        # Run agent
        context = {'dataset_id': req.dataset_id} if req.dataset_id else {}
        result = await agent.run(req.query, context)
        
        execution_time = time.time() - start_time
        
        # Update query record
        QueryRepository.update_query_result(
            db=db,
            query_id=query_record.id,
            status=result['status'],
            explanation=result.get('output', ''),
            execution_time=execution_time
        )
        
        return QueryResponse(
            job_id=str(query_record.id),
            status=result['status'],
            explanation=result.get('output', ''),
            error=result.get('error')
        )
        
    except Exception as e:
        QueryRepository.update_query_result(
            db=db,
            query_id=query_record.id,
            status='error',
            explanation=str(e)
        )
        raise HTTPException(status_code=500, detail=str(e))
