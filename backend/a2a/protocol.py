"""
Agent-to-Agent (A2A) Messaging Protocol
"""
import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel

class MessageType(str, Enum):
    TASK_REQUEST = "TASK_REQUEST"
    TASK_STATUS = "TASK_STATUS"
    TASK_RESULT = "TASK_RESULT"
    APPROVAL_REQUEST = "APPROVAL_REQUEST"
    APPROVAL_RESPONSE = "APPROVAL_RESPONSE"
    ERROR = "ERROR"

class A2AMessage(BaseModel):
    """A2A message envelope"""
    message_id: str
    type: MessageType
    from_agent: str
    to_agent: str
    timestamp: str
    trace_id: str
    payload: Dict[str, Any]
    signature: Optional[str] = None
    
    @classmethod
    def create(
        cls,
        msg_type: MessageType,
        from_agent: str,
        to_agent: str,
        payload: Dict[str, Any],
        trace_id: Optional[str] = None
    ) -> "A2AMessage":
        """Create a new A2A message"""
        return cls(
            message_id=str(uuid.uuid4()),
            type=msg_type,
            from_agent=from_agent,
            to_agent=to_agent,
            timestamp=datetime.utcnow().isoformat() + "Z",
            trace_id=trace_id or str(uuid.uuid4()),
            payload=payload
        )
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return self.model_dump_json()
    
    @classmethod
    def from_json(cls, json_str: str) -> "A2AMessage":
        """Create from JSON string"""
        return cls.model_validate_json(json_str)

class TaskRequest(BaseModel):
    """Payload for TASK_REQUEST"""
    task_id: str
    tool_id: str
    inputs: Dict[str, Any]
    metadata: Dict[str, Any] = {}

class TaskStatus(BaseModel):
    """Payload for TASK_STATUS"""
    task_id: str
    status: str  # queued, running, completed, failed, paused
    progress: Optional[float] = None  # 0.0 to 1.0
    message: Optional[str] = None
    logs: Optional[str] = None

class TaskResult(BaseModel):
    """Payload for TASK_RESULT"""
    task_id: str
    status: str  # completed or failed
    outputs: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    artifacts: Optional[list] = []

class ApprovalRequest(BaseModel):
    """Payload for APPROVAL_REQUEST"""
    task_id: str
    reason: str
    artifacts: list = []
    estimated_risk: str = "medium"  # low, medium, high
    approvers: list = []

class ApprovalResponse(BaseModel):
    """Payload for APPROVAL_RESPONSE"""
    task_id: str
    approver_id: str
    decision: bool  # True = approve, False = reject
    notes: Optional[str] = None

def create_task_request(
    from_agent: str,
    to_agent: str,
    task_id: str,
    tool_id: str,
    inputs: Dict[str, Any],
    trace_id: Optional[str] = None
) -> A2AMessage:
    """Helper to create TASK_REQUEST message"""
    payload = TaskRequest(
        task_id=task_id,
        tool_id=tool_id,
        inputs=inputs
    ).model_dump()
    
    return A2AMessage.create(
        msg_type=MessageType.TASK_REQUEST,
        from_agent=from_agent,
        to_agent=to_agent,
        payload=payload,
        trace_id=trace_id
    )

def create_task_status(
    from_agent: str,
    to_agent: str,
    task_id: str,
    status: str,
    progress: Optional[float] = None,
    message: Optional[str] = None,
    trace_id: Optional[str] = None
) -> A2AMessage:
    """Helper to create TASK_STATUS message"""
    payload = TaskStatus(
        task_id=task_id,
        status=status,
        progress=progress,
        message=message
    ).model_dump()
    
    return A2AMessage.create(
        msg_type=MessageType.TASK_STATUS,
        from_agent=from_agent,
        to_agent=to_agent,
        payload=payload,
        trace_id=trace_id
    )

def create_task_result(
    from_agent: str,
    to_agent: str,
    task_id: str,
    status: str,
    outputs: Optional[Dict[str, Any]] = None,
    error: Optional[str] = None,
    trace_id: Optional[str] = None
) -> A2AMessage:
    """Helper to create TASK_RESULT message"""
    payload = TaskResult(
        task_id=task_id,
        status=status,
        outputs=outputs,
        error=error
    ).model_dump()
    
    return A2AMessage.create(
        msg_type=MessageType.TASK_RESULT,
        from_agent=from_agent,
        to_agent=to_agent,
        payload=payload,
        trace_id=trace_id
    )
