"""
Unit tests for user service layer.
"""

import pytest
from fastapi import HTTPException

from app.models.post import Post
from app.models.user import User
from app.services.user import get_user_profile


@pytest.mark.asyncio
async def test_get_user_profile(test_user: User):
    """Test getting a user profile."""
    # Create some posts for the user
    await Post.create(title="Post 1", content="Content 1", author=test_user)
    await Post.create(title="Post 2", content="Content 2", author=test_user)

    profile = await get_user_profile(test_user.id)

    assert profile["id"] == test_user.id
    assert profile["username"] == test_user.username
    assert profile["post_count"] == 2
    assert "created_at" in profile


@pytest.mark.asyncio
async def test_get_user_profile_no_posts(test_user: User):
    """Test getting a user profile with no posts."""
    profile = await get_user_profile(test_user.id)

    assert profile["id"] == test_user.id
    assert profile["username"] == test_user.username
    assert profile["post_count"] == 0


@pytest.mark.asyncio
async def test_get_user_profile_not_found():
    """Test getting a non-existent user profile returns 404."""
    with pytest.raises(HTTPException) as exc_info:
        await get_user_profile(99999)

    assert exc_info.value.status_code == 404
    assert "user not found" in exc_info.value.detail.lower()

