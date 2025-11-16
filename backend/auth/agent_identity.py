"""
Agent Identity & JWT Token Management
"""
import jwt
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import secrets

# Secret key for JWT signing (in production, use environment variable)
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"

class AgentIdentity:
    """Manages agent identities and JWT tokens"""
    
    def __init__(self, agent_id: str, agent_type: str, roles: List[str], scopes: List[str]):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.roles = roles
        self.scopes = scopes
    
    def generate_token(self, expires_in_hours: int = 24) -> str:
        """Generate JWT token for this agent"""
        payload = {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "roles": self.roles,
            "scopes": self.scopes,
            "iss": "auth-server",
            "sub": self.agent_id,
            "iat": int(time.time()),
            "exp": int((datetime.utcnow() + timedelta(hours=expires_in_hours)).timestamp())
        }
        
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    @staticmethod
    def has_scope(token_payload: Dict, required_scope: str) -> bool:
        """Check if token has required scope"""
        scopes = token_payload.get('scopes', [])
        return required_scope in scopes
    
    @staticmethod
    def has_role(token_payload: Dict, required_role: str) -> bool:
        """Check if token has required role"""
        roles = token_payload.get('roles', [])
        return required_role in roles

# Predefined agent identities
PLANNER_AGENT = AgentIdentity(
    agent_id="planner.agent.v1",
    agent_type="planner",
    roles=["planner"],
    scopes=["tools:discover", "plans:create", "tasks:create"]
)

EXECUTOR_AGENT = AgentIdentity(
    agent_id="executor.agent.v1",
    agent_type="executor",
    roles=["executor"],
    scopes=["tools:invoke", "executor:run", "datasets:read"]
)

EVALUATOR_AGENT = AgentIdentity(
    agent_id="evaluator.agent.v1",
    agent_type="evaluator",
    roles=["evaluator"],
    scopes=["evaluations:create", "tasks:read"]
)

def create_agent_token(agent_type: str) -> str:
    """Create token for a specific agent type"""
    agents = {
        "planner": PLANNER_AGENT,
        "executor": EXECUTOR_AGENT,
        "evaluator": EVALUATOR_AGENT
    }
    
    agent = agents.get(agent_type)
    if not agent:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    return agent.generate_token()
