"""
User-related API endpoints.

This module provides RESTful API routes for user profile operations.
"""

from fastapi import APIRouter

from app.services.user import get_user_profile

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/{user_id}")
async def get_user(user_id: int):
    """
    Get a user's public profile.

    Args:
        user_id: ID of the user

    Returns:
        User profile with post count
    """
    profile = await get_user_profile(user_id)
    return profile

