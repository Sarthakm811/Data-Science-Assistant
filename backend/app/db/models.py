"""
SQLAlchemy models for PostgreSQL
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.sql import func
from app.db.database import Base

class Query(Base):
    """Store user queries and responses"""
    __tablename__ = "queries"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    user_id = Column(String(255), index=True, nullable=True)
    query_text = Column(Text, nullable=False)
    dataset_id = Column(String(255), nullable=True)
    
    # Response data
    status = Column(String(50))
    plan = Column(Text)
    code = Column(Text)
    results = Column(JSON)
    explanation = Column(Text)
    
    # Metadata
    execution_time = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Dataset(Base):
    """Cache dataset metadata"""
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(String(255), unique=True, index=True)
    title = Column(String(500))
    description = Column(Text)
    size = Column(Integer)
    columns = Column(JSON)
    url = Column(String(500))
    
    # Metadata
    last_accessed = Column(DateTime(timezone=True))
    access_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class APILog(Base):
    """Log all API requests"""
    __tablename__ = "api_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String(255))
    method = Column(String(10))
    status_code = Column(Integer)
    
    # Request/Response
    request_body = Column(JSON)
    response_body = Column(JSON)
    
    # Performance
    duration_ms = Column(Float)
    
    # User context
    session_id = Column(String(255), index=True)
    user_id = Column(String(255), index=True, nullable=True)
    ip_address = Column(String(50))
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Session(Base):
    """Store session information"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, index=True)
    user_id = Column(String(255), index=True, nullable=True)
    
    # Session data
    current_dataset = Column(String(255))
    context = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), onupdate=func.now())
