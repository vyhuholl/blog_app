"""
Pytest configuration and shared fixtures.

This module sets up the test environment with database initialization,
test client, and fixture factories for creating test data.
"""

import asyncio
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.main import app
from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.services.auth import hash_password


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def init_db():
    """Initialize database for tests with in-memory SQLite."""
    await initializer(
        modules=["app.models.user", "app.models.post", "app.models.comment"],
        db_url="sqlite://:memory:",
        app_label="models",
    )
    yield
    await finalizer()


@pytest.fixture
def client() -> TestClient:
    """Create a test client for FastAPI application."""
    return TestClient(app)


@pytest.fixture
async def test_user():
    """Create a test user."""
    password_hash = await hash_password("testpass123")
    user = await User.create(
        username="testuser", email="test@example.com", password_hash=password_hash
    )
    return user


@pytest.fixture
async def test_user_2():
    """Create a second test user."""
    password_hash = await hash_password("testpass456")
    user = await User.create(
        username="testuser2", email="test2@example.com", password_hash=password_hash
    )
    return user


@pytest.fixture
async def test_post(test_user):
    """Create a test post."""
    post = await Post.create(
        title="Test Post", content="This is test post content.", author=test_user
    )
    return post


@pytest.fixture
async def test_comment(test_post, test_user_2):
    """Create a test comment."""
    comment = await Comment.create(
        content="This is a test comment.", post=test_post, author=test_user_2
    )
    return comment

