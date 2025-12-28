"""
Tests for authentication dependency.

Tests the get_current_user dependency for extracting and validating
authenticated users from JWT tokens.
"""

import pytest
from fastapi import HTTPException

from app.dependencies.auth import get_current_user
from app.services.auth import create_access_token


class TestAuthDependency:
    """Test authentication dependency."""

    @pytest.mark.asyncio
    async def test_get_current_user_success(self, test_user):
        """Test get_current_user with valid token."""
        token = create_access_token(test_user.id)

        user = await get_current_user(access_token=token)

        assert user.id == test_user.id
        assert user.username == test_user.username

    @pytest.mark.asyncio
    async def test_get_current_user_no_token(self):
        """Test get_current_user without token raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(access_token=None)

        assert exc_info.value.status_code == 401
        assert "Not authenticated" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self):
        """Test get_current_user with invalid token raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(access_token="invalid-token")

        assert exc_info.value.status_code == 401

    @pytest.mark.asyncio
    async def test_get_current_user_nonexistent_user(self):
        """Test get_current_user with valid token but nonexistent user."""
        token = create_access_token(999999)  # Non-existent user ID

        with pytest.raises(HTTPException) as exc_info:
            await get_current_user(access_token=token)

        assert exc_info.value.status_code == 401
        assert "User not found" in exc_info.value.detail

