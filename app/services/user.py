"""
User service layer.

This module provides business logic for user-related operations such as
fetching user profiles.
"""

from fastapi import HTTPException, status

from app.models.user import User


async def get_user_profile(user_id: int) -> dict:
    """
    Get a user's public profile with post count.

    Args:
        user_id: ID of the user

    Returns:
        Dictionary with user profile information

    Raises:
        HTTPException: If user not found
    """
    user = await User.filter(id=user_id).prefetch_related("posts").first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Count posts
    post_count = await user.posts.all().count()

    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at,
        "post_count": post_count,
    }

