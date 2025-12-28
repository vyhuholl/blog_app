"""
Test Pydantic schemas for validation.

This module tests that Pydantic schemas validate data correctly.
These are pure validation tests that don't require database access.
"""

import pytest
from pydantic import ValidationError

from app.schemas.comment import CommentCreate, CommentUpdate
from app.schemas.post import PostCreate, PostUpdate
from app.schemas.user import UserLogin, UserRegister


# Disable database fixture for these tests
pytestmark = pytest.mark.asyncio(scope="module")


class TestUserSchemas:
    """Test User-related schemas."""

    def test_user_register_valid(self):
        """Test valid user registration data."""
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }
        schema = UserRegister(**data)
        assert schema.username == "testuser"
        assert schema.email == "test@example.com"
        assert schema.password == "password123"

    def test_user_register_invalid_username(self):
        """Test user registration with invalid username."""
        with pytest.raises(ValidationError):
            UserRegister(
                username="ab",  # Too short
                email="test@example.com",
                password="password123",
            )

    def test_user_register_invalid_email(self):
        """Test user registration with invalid email."""
        with pytest.raises(ValidationError):
            UserRegister(username="testuser", email="notanemail", password="password123")

    def test_user_register_short_password(self):
        """Test user registration with short password."""
        with pytest.raises(ValidationError):
            UserRegister(username="testuser", email="test@example.com", password="short")

    def test_user_login_valid(self):
        """Test valid user login data."""
        data = {"username": "testuser", "password": "password123"}
        schema = UserLogin(**data)
        assert schema.username == "testuser"
        assert schema.password == "password123"


class TestPostSchemas:
    """Test Post-related schemas."""

    def test_post_create_valid(self):
        """Test valid post creation data."""
        data = {"title": "Test Post", "content": "This is test content."}
        schema = PostCreate(**data)
        assert schema.title == "Test Post"
        assert schema.content == "This is test content."

    def test_post_create_empty_title(self):
        """Test post creation with empty title."""
        with pytest.raises(ValidationError):
            PostCreate(title="", content="Content")

    def test_post_create_long_title(self):
        """Test post creation with overly long title."""
        with pytest.raises(ValidationError):
            PostCreate(title="a" * 201, content="Content")

    def test_post_update_valid(self):
        """Test valid post update data."""
        data = {"title": "Updated Title", "content": "Updated content."}
        schema = PostUpdate(**data)
        assert schema.title == "Updated Title"
        assert schema.content == "Updated content."


class TestCommentSchemas:
    """Test Comment-related schemas."""

    def test_comment_create_valid(self):
        """Test valid comment creation data."""
        data = {"content": "This is a comment."}
        schema = CommentCreate(**data)
        assert schema.content == "This is a comment."

    def test_comment_create_empty_content(self):
        """Test comment creation with empty content."""
        with pytest.raises(ValidationError):
            CommentCreate(content="")

    def test_comment_create_long_content(self):
        """Test comment creation with overly long content."""
        with pytest.raises(ValidationError):
            CommentCreate(content="a" * 1001)

    def test_comment_update_valid(self):
        """Test valid comment update data."""
        data = {"content": "Updated comment text."}
        schema = CommentUpdate(**data)
        assert schema.content == "Updated comment text."

