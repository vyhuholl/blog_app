"""
Integration tests for users API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.models.post import Post
from app.models.user import User


@pytest.mark.asyncio
async def test_get_user_profile_success(client: TestClient, test_user: User):
    """Test get user profile returns public information."""
    # Create some posts for the user
    await Post.create(title="Post 1", content="Content 1", author=test_user)
    await Post.create(title="Post 2", content="Content 2", author=test_user)

    response = client.get(f"/api/users/{test_user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["post_count"] == 2
    assert "created_at" in data
    # Should not expose sensitive data
    assert "email" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_get_user_profile_no_posts(client: TestClient, test_user: User):
    """Test get user profile with no posts."""
    response = client.get(f"/api/users/{test_user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["post_count"] == 0


@pytest.mark.asyncio
async def test_get_user_profile_not_found(client: TestClient):
    """Test get non-existent user profile returns 404."""
    response = client.get("/api/users/99999")

    assert response.status_code == 404
    assert "user not found" in response.json()["detail"].lower()

