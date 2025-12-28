"""
Tests for authentication service layer.

Tests password hashing, JWT token creation/verification, user registration,
and user authentication.
"""

import pytest
from fastapi import HTTPException

from app.services.auth import (
    authenticate_user,
    create_access_token,
    decode_access_token,
    hash_password,
    register_user,
    verify_password,
)


class TestPasswordHashing:
    """Test password hashing functions."""

    @pytest.mark.asyncio
    async def test_hash_password(self):
        """Test password hashing produces valid bcrypt hash."""
        password = "testpass123"
        hashed = await hash_password(password)

        assert hashed.startswith("$2b$")
        assert len(hashed) > 50

    @pytest.mark.asyncio
    async def test_verify_password_success(self):
        """Test password verification with correct password."""
        password = "testpass123"
        hashed = await hash_password(password)

        assert await verify_password(password, hashed) is True

    @pytest.mark.asyncio
    async def test_verify_password_failure(self):
        """Test password verification with incorrect password."""
        password = "testpass123"
        hashed = await hash_password(password)

        assert await verify_password("wrongpassword", hashed) is False


class TestJWTTokens:
    """Test JWT token creation and verification."""

    def test_create_access_token(self):
        """Test JWT token creation."""
        user_id = 1
        token = create_access_token(user_id)

        assert isinstance(token, str)
        assert len(token) > 20

    def test_decode_access_token(self):
        """Test JWT token decoding."""
        user_id = 1
        token = create_access_token(user_id)

        payload = decode_access_token(token)

        assert payload["user_id"] == user_id
        assert "exp" in payload

    def test_decode_invalid_token(self):
        """Test decoding invalid token raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            decode_access_token("invalid-token")

        assert exc_info.value.status_code == 401
        assert "Invalid token" in exc_info.value.detail


class TestUserRegistration:
    """Test user registration logic."""

    @pytest.mark.asyncio
    async def test_register_user_success(self):
        """Test successful user registration."""
        user = await register_user("newuser", "new@example.com", "password123")

        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.password_hash.startswith("$2b$")

    @pytest.mark.asyncio
    async def test_register_duplicate_username(self, test_user):
        """Test registration with duplicate username raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            await register_user(test_user.username, "different@example.com", "password123")

        assert exc_info.value.status_code == 409
        assert "Username already exists" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, test_user):
        """Test registration with duplicate email raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            await register_user("differentuser", test_user.email, "password123")

        assert exc_info.value.status_code == 409
        assert "Email already exists" in exc_info.value.detail


class TestUserAuthentication:
    """Test user authentication logic."""

    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, test_user):
        """Test successful user authentication."""
        user = await authenticate_user("testuser", "testpass123")

        assert user.id == test_user.id
        assert user.username == test_user.username

    @pytest.mark.asyncio
    async def test_authenticate_invalid_username(self):
        """Test authentication with invalid username raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            await authenticate_user("nonexistentuser", "password")

        assert exc_info.value.status_code == 401
        assert "Invalid username or password" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_authenticate_invalid_password(self, test_user):
        """Test authentication with invalid password raises exception."""
        with pytest.raises(HTTPException) as exc_info:
            await authenticate_user(test_user.username, "wrongpassword")

        assert exc_info.value.status_code == 401
        assert "Invalid username or password" in exc_info.value.detail

