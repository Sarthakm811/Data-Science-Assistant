"""
Role-Based Access Control (RBAC)
"""

from typing import List, Dict, Set
from enum import Enum


class Role(str, Enum):
    USER = "user"
    RESEARCHER = "researcher"
    AGENT_PLANNER = "agent_planner"
    AGENT_EXECUTOR = "agent_executor"
    AGENT_EVALUATOR = "agent_evaluator"
    ADMIN = "admin"


class Permission(str, Enum):
    # Tool permissions
    TOOLS_DISCOVER = "tools:discover"
    TOOLS_INVOKE = "tools:invoke"

    # Dataset permissions
    DATASETS_READ = "datasets:read"
    DATASETS_WRITE = "datasets:write"

    # Task permissions
    TASKS_CREATE = "tasks:create"
    TASKS_READ = "tasks:read"
    TASKS_UPDATE = "tasks:update"
    TASKS_DELETE = "tasks:delete"

    # Execution permissions
    EXECUTOR_RUN = "executor:run"
    ANALYZER_RUN = "analyzer:run"

    # Approval permissions
    APPROVALS_APPROVE = "approvals:approve"
    APPROVALS_REJECT = "approvals:reject"

    # Plan permissions
    PLANS_CREATE = "plans:create"
    PLANS_READ = "plans:read"

    # Evaluation permissions
    EVALUATIONS_CREATE = "evaluations:create"
    EVALUATIONS_READ = "evaluations:read"


# Role to permissions mapping
ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.USER: {
        Permission.TOOLS_DISCOVER,
        Permission.DATASETS_READ,
        Permission.TASKS_READ,
    },
    Role.RESEARCHER: {
        Permission.TOOLS_DISCOVER,
        Permission.TOOLS_INVOKE,
        Permission.DATASETS_READ,
        Permission.DATASETS_WRITE,
        Permission.TASKS_CREATE,
        Permission.TASKS_READ,
        Permission.PLANS_READ,
        Permission.EVALUATIONS_READ,
    },
    Role.AGENT_PLANNER: {
        Permission.TOOLS_DISCOVER,
        Permission.PLANS_CREATE,
        Permission.PLANS_READ,
        Permission.TASKS_CREATE,
        Permission.TASKS_READ,
    },
    Role.AGENT_EXECUTOR: {
        Permission.TOOLS_INVOKE,
        Permission.EXECUTOR_RUN,
        Permission.ANALYZER_RUN,
        Permission.DATASETS_READ,
        Permission.TASKS_READ,
        Permission.TASKS_UPDATE,
    },
    Role.AGENT_EVALUATOR: {
        Permission.EVALUATIONS_CREATE,
        Permission.EVALUATIONS_READ,
        Permission.TASKS_READ,
    },
    Role.ADMIN: set(Permission),  # All permissions
}


class RBACService:
    """RBAC enforcement service"""

    @staticmethod
    def get_permissions(roles: List[str]) -> Set[str]:
        """Get all permissions for given roles"""
        permissions = set()
        for role_str in roles:
            try:
                role = Role(role_str)
                permissions.update(ROLE_PERMISSIONS.get(role, set()))
            except ValueError:
                continue
        return permissions

    @staticmethod
    def has_permission(roles: List[str], required_permission: str) -> bool:
        """Check if roles have required permission"""
        permissions = RBACService.get_permissions(roles)
        return required_permission in permissions

    @staticmethod
    def check_tool_access(roles: List[str], tool_scopes: List[str]) -> bool:
        """Check if roles have access to tool based on scopes"""
        user_permissions = RBACService.get_permissions(roles)

        # Check if user has any of the required scopes
        for scope in tool_scopes:
            if scope in user_permissions:
                return True

        return False


# Global RBAC service instance
rbac_service = RBACService()
