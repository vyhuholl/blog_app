"""
Authentication dependencies for FastAPI routes.

This module provides FastAPI dependencies for extracting and validating
the current authenticated user from JWT tokens.
"""

from fastapi import Cookie, Depends, HTTPException, status

from app.models.user import User
from app.services.auth import decode_access_token


async def get_current_user(access_token: str | None = Cookie(None)) -> User:
    """
    Extract and validate current user from JWT cookie.

    Args:
        access_token: JWT token from HTTP-only cookie

    Returns:
        Current authenticated User object

    Raises:
        HTTPException: If token is missing, invalid, or user not found
    """
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    # Decode token to get user_id
    payload = decode_access_token(access_token)
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload"
        )

    # Fetch user from database
    user = await User.filter(id=user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )

    return user


# Alias for cleaner imports
CurrentUser = Depends(get_current_user)

