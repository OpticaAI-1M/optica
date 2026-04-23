"""
JWT validation using Keycloak public keys.
"""

from typing import Any, Dict

import requests
from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTError


KEYCLOAK_URL = "http://keycloak:8080"
REALM = "optica"
ALGORITHM = "RS256"


def get_public_key() -> str:
    """
    Fetch Keycloak public key for verifying JWT.
    """
    url = f"{KEYCLOAK_URL}/realms/{REALM}"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Failed to fetch Keycloak public key")

    public_key = response.json()["public_key"]

    return f"-----BEGIN PUBLIC KEY-----\n{public_key}\n-----END PUBLIC KEY-----"


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and return decoded payload.
    """
    try:
        public_key = get_public_key()

        payload = jwt.decode(
            token,
            public_key,
            algorithms=[ALGORITHM],
            audience="account",
        )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )