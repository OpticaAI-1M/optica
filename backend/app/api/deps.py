"""
Authentication dependencies for FastAPI routes.
"""

from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_token


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """
    Extract and validate current user from JWT token.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization credentials",
        )

    token = credentials.credentials

    payload = verify_token(token)

    return payload

def require_roles(required_roles: list[str]):
    """
    Dependency factory to enforce role-based access.
    """

    def role_checker(user: dict = Depends(get_current_user)):
        user_roles = user.get("realm_access", {}).get("roles", [])

        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return user

    return role_checker