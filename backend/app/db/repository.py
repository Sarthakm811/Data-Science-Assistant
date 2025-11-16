"""
Database repository layer for queries and logs
"""

from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime
import logging

from app.db.models import Query, Dataset, APILog, Session as SessionModel

logger = logging.getLogger(__name__)


class QueryRepository:
    """Repository for query operations"""

    @staticmethod
    def create_query(
        db: Session,
        session_id: str,
        query_text: str,
        dataset_id: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Query:
        """Create new query record"""
        query = Query(
            session_id=session_id,
            user_id=user_id,
            query_text=query_text,
            dataset_id=dataset_id,
            status="pending",
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query

    @staticmethod
    def update_query_result(
        db: Session,
        query_id: int,
        status: str,
        plan: str = None,
        code: str = None,
        results: Dict = None,
        explanation: str = None,
        execution_time: float = None,
    ):
        """Update query with results"""
        query = db.query(Query).filter(Query.id == query_id).first()
        if query:
            query.status = status
            query.plan = plan
            query.code = code
            query.results = results
            query.explanation = explanation
            query.execution_time = execution_time
            db.commit()

    @staticmethod
    def get_session_queries(
        db: Session, session_id: str, limit: int = 10
    ) -> List[Query]:
        """Get recent queries for a session"""
        return (
            db.query(Query)
            .filter(Query.session_id == session_id)
            .order_by(Query.created_at.desc())
            .limit(limit)
            .all()
        )


class DatasetRepository:
    """Repository for dataset metadata"""

    @staticmethod
    def upsert_dataset(
        db: Session,
        dataset_id: str,
        title: str,
        description: str = None,
        size: int = None,
        columns: List = None,
        url: str = None,
    ) -> Dataset:
        """Create or update dataset metadata"""
        dataset = db.query(Dataset).filter(Dataset.dataset_id == dataset_id).first()

        if dataset:
            dataset.title = title
            dataset.description = description
            dataset.size = size
            dataset.columns = columns
            dataset.url = url
            dataset.last_accessed = datetime.utcnow()
            dataset.access_count += 1
        else:
            dataset = Dataset(
                dataset_id=dataset_id,
                title=title,
                description=description,
                size=size,
                columns=columns,
                url=url,
                last_accessed=datetime.utcnow(),
                access_count=1,
            )
            db.add(dataset)

        db.commit()
        db.refresh(dataset)
        return dataset

    @staticmethod
    def get_popular_datasets(db: Session, limit: int = 10) -> List[Dataset]:
        """Get most accessed datasets"""
        return (
            db.query(Dataset).order_by(Dataset.access_count.desc()).limit(limit).all()
        )


class APILogRepository:
    """Repository for API logging"""

    @staticmethod
    def log_request(
        db: Session,
        endpoint: str,
        method: str,
        status_code: int,
        duration_ms: float,
        session_id: str = None,
        user_id: str = None,
        ip_address: str = None,
        request_body: Dict = None,
        response_body: Dict = None,
    ):
        """Log API request"""
        log = APILog(
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            duration_ms=duration_ms,
            session_id=session_id,
            user_id=user_id,
            ip_address=ip_address,
            request_body=request_body,
            response_body=response_body,
        )
        db.add(log)
        db.commit()


class SessionRepository:
    """Repository for session management"""

    @staticmethod
    def create_session(
        db: Session, session_id: str, user_id: Optional[str] = None
    ) -> SessionModel:
        """Create new session"""
        session = SessionModel(session_id=session_id, user_id=user_id, context={})
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def update_session(
        db: Session, session_id: str, current_dataset: str = None, context: Dict = None
    ):
        """Update session data"""
        session = (
            db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        )
        if session:
            if current_dataset:
                session.current_dataset = current_dataset
            if context:
                session.context = context
            session.last_activity = datetime.utcnow()
            db.commit()
