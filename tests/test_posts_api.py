"""
Integration tests for posts API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.models.post import Post
from app.models.user import User
from app.services.auth import create_access_token


@pytest.mark.asyncio
async def test_create_post_success(client: TestClient, test_user: User):
    """Test authenticated user can create post."""
    token = create_access_token(test_user.id)

    response = client.post(
        "/api/posts",
        json={"title": "New Post", "content": "This is new post content."},
        cookies={"access_token": token},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "New Post"
    assert data["content"] == "This is new post content."
    assert data["author"]["username"] == test_user.username


@pytest.mark.asyncio
async def test_create_post_unauthorized(client: TestClient):
    """Test unauthenticated user cannot create post."""
    response = client.post(
        "/api/posts", json={"title": "New Post", "content": "This is new post content."}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_posts_pagination(client: TestClient, test_user: User):
    """Test get posts with pagination."""
    # Create some posts
    for i in range(5):
        await Post.create(
            title=f"Post {i}", content=f"Content {i}", author=test_user
        )

    response = client.get("/api/posts?page=1&page_size=3")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    assert data["total"] == 5
    assert data["page"] == 1
    assert data["page_size"] == 3
    assert data["total_pages"] == 2


@pytest.mark.asyncio
async def test_get_posts_default_pagination(client: TestClient):
    """Test get posts with default pagination."""
    response = client.get("/api/posts")

    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert data["page"] == 1
    assert data["page_size"] == 20


@pytest.mark.asyncio
async def test_get_post_success(client: TestClient, test_post: Post):
    """Test get single post by ID."""
    response = client.get(f"/api/posts/{test_post.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == test_post.title
    assert data["content"] == test_post.content


@pytest.mark.asyncio
async def test_get_post_not_found(client: TestClient):
    """Test get non-existent post returns 404."""
    response = client.get("/api/posts/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_post_by_author_success(
    client: TestClient, test_user: User, test_post: Post
):
    """Test post author can update their post."""
    token = create_access_token(test_user.id)

    response = client.put(
        f"/api/posts/{test_post.id}",
        json={"title": "Updated Title", "content": "Updated content."},
        cookies={"access_token": token},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_post.id
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content."


@pytest.mark.asyncio
async def test_update_post_by_non_author_forbidden(
    client: TestClient, test_user_2: User, test_post: Post
):
    """Test non-author cannot update post."""
    token = create_access_token(test_user_2.id)

    response = client.put(
        f"/api/posts/{test_post.id}",
        json={"title": "Hacked Title", "content": "Hacked content."},
        cookies={"access_token": token},
    )

    assert response.status_code == 403
    assert "author" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_post_unauthorized(client: TestClient, test_post: Post):
    """Test unauthenticated user cannot update post."""
    response = client.put(
        f"/api/posts/{test_post.id}",
        json={"title": "Updated Title", "content": "Updated content."},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_post_not_found(client: TestClient, test_user: User):
    """Test updating non-existent post returns 404."""
    token = create_access_token(test_user.id)

    response = client.put(
        "/api/posts/99999",
        json={"title": "Test", "content": "Test"},
        cookies={"access_token": token},
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_post_by_author_success(
    client: TestClient, test_user: User, test_post: Post
):
    """Test post author can delete their post."""
    token = create_access_token(test_user.id)
    post_id = test_post.id

    response = client.delete(f"/api/posts/{post_id}", cookies={"access_token": token})

    assert response.status_code == 204

    # Verify post is deleted
    deleted_post = await Post.filter(id=post_id).first()
    assert deleted_post is None


@pytest.mark.asyncio
async def test_delete_post_by_non_author_forbidden(
    client: TestClient, test_user: User, test_user_2: User
):
    """Test non-author cannot delete post."""
    # Create a post by test_user
    post = await Post.create(
        title="Test Post", content="Test content.", author=test_user
    )

    token = create_access_token(test_user_2.id)

    response = client.delete(f"/api/posts/{post.id}", cookies={"access_token": token})

    assert response.status_code == 403
    assert "author" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_delete_post_unauthorized(client: TestClient, test_post: Post):
    """Test unauthenticated user cannot delete post."""
    response = client.delete(f"/api/posts/{test_post.id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_post_not_found(client: TestClient, test_user: User):
    """Test deleting non-existent post returns 404."""
    token = create_access_token(test_user.id)

    response = client.delete("/api/posts/99999", cookies={"access_token": token})

    assert response.status_code == 404

