"""
Integration tests for comments API endpoints.
"""

import pytest
from fastapi.testclient import TestClient

from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.services.auth import create_access_token


@pytest.mark.asyncio
async def test_create_comment_success(client: TestClient, test_post: Post, test_user: User):
    """Test authenticated user can create comment."""
    token = create_access_token(test_user.id)

    response = client.post(
        f"/api/posts/{test_post.id}/comments",
        json={"content": "Great post!"},
        cookies={"access_token": token},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Great post!"
    assert data["post_id"] == test_post.id
    assert data["author"]["username"] == test_user.username


@pytest.mark.asyncio
async def test_create_comment_unauthorized(client: TestClient, test_post: Post):
    """Test unauthenticated user cannot create comment."""
    response = client.post(
        f"/api/posts/{test_post.id}/comments", json={"content": "Great post!"}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_comment_on_nonexistent_post(client: TestClient, test_user: User):
    """Test creating comment on non-existent post returns 404."""
    token = create_access_token(test_user.id)

    response = client.post(
        "/api/posts/99999/comments",
        json={"content": "Great post!"},
        cookies={"access_token": token},
    )

    assert response.status_code == 404
    assert "post not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_post_comments_chronological_order(
    client: TestClient, test_post: Post, test_user: User, test_user_2: User
):
    """Test comments are returned in chronological order (oldest first)."""
    # Create comments
    await Comment.create(content="First comment", post=test_post, author=test_user)
    await Comment.create(content="Second comment", post=test_post, author=test_user_2)
    await Comment.create(content="Third comment", post=test_post, author=test_user)

    response = client.get(f"/api/posts/{test_post.id}/comments")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    # Verify ordering (oldest first)
    assert data[0]["content"] == "First comment"
    assert data[1]["content"] == "Second comment"
    assert data[2]["content"] == "Third comment"


@pytest.mark.asyncio
async def test_get_post_comments_empty(client: TestClient, test_post: Post):
    """Test get comments for post with no comments."""
    response = client.get(f"/api/posts/{test_post.id}/comments")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.asyncio
async def test_update_comment_by_author_success(
    client: TestClient, test_user: User, test_post: Post
):
    """Test comment author can update their comment."""
    comment = await Comment.create(
        content="Original content", post=test_post, author=test_user
    )
    token = create_access_token(test_user.id)

    response = client.put(
        f"/api/comments/{comment.id}",
        json={"content": "Updated content"},
        cookies={"access_token": token},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == comment.id
    assert data["content"] == "Updated content"


@pytest.mark.asyncio
async def test_update_comment_by_non_author_forbidden(
    client: TestClient, test_user: User, test_user_2: User, test_post: Post
):
    """Test non-author cannot update comment."""
    comment = await Comment.create(
        content="Original content", post=test_post, author=test_user
    )
    token = create_access_token(test_user_2.id)

    response = client.put(
        f"/api/comments/{comment.id}",
        json={"content": "Hacked content"},
        cookies={"access_token": token},
    )

    assert response.status_code == 403
    assert "author" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_comment_unauthorized(client: TestClient, test_post: Post):
    """Test unauthenticated user cannot update comment."""
    comment = await Comment.create(
        content="Test content", post=test_post, author=test_post.author
    )

    response = client.put(
        f"/api/comments/{comment.id}", json={"content": "Updated content"}
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_comment_not_found(client: TestClient, test_user: User):
    """Test updating non-existent comment returns 404."""
    token = create_access_token(test_user.id)

    response = client.put(
        "/api/comments/99999", json={"content": "Test"}, cookies={"access_token": token}
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_comment_by_author_success(
    client: TestClient, test_user: User, test_post: Post
):
    """Test comment author can delete their comment."""
    comment = await Comment.create(content="Test comment", post=test_post, author=test_user)
    token = create_access_token(test_user.id)
    comment_id = comment.id

    response = client.delete(f"/api/comments/{comment_id}", cookies={"access_token": token})

    assert response.status_code == 204

    # Verify comment is deleted
    deleted_comment = await Comment.filter(id=comment_id).first()
    assert deleted_comment is None


@pytest.mark.asyncio
async def test_delete_comment_by_non_author_forbidden(
    client: TestClient, test_user: User, test_user_2: User, test_post: Post
):
    """Test non-author cannot delete comment."""
    comment = await Comment.create(content="Test comment", post=test_post, author=test_user)
    token = create_access_token(test_user_2.id)

    response = client.delete(f"/api/comments/{comment.id}", cookies={"access_token": token})

    assert response.status_code == 403
    assert "author" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_delete_comment_unauthorized(client: TestClient, test_post: Post):
    """Test unauthenticated user cannot delete comment."""
    comment = await Comment.create(
        content="Test content", post=test_post, author=test_post.author
    )

    response = client.delete(f"/api/comments/{comment.id}")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_comment_not_found(client: TestClient, test_user: User):
    """Test deleting non-existent comment returns 404."""
    token = create_access_token(test_user.id)

    response = client.delete("/api/comments/99999", cookies={"access_token": token})

    assert response.status_code == 404

