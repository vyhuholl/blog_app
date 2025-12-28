"""
Unit tests for post service layer.
"""

import pytest
from fastapi import HTTPException

from app.models.post import Post
from app.models.user import User
from app.services.post import (
    check_post_author,
    create_post,
    delete_post,
    get_post_by_id,
    list_posts,
    update_post,
)


@pytest.mark.asyncio
async def test_create_post(test_user: User):
    """Test creating a post."""
    post = await create_post(title="Test Post", content="Test content", author=test_user)

    assert post.title == "Test Post"
    assert post.content == "Test content"
    assert post.author.id == test_user.id
    assert post.id is not None


@pytest.mark.asyncio
async def test_create_post_empty_title(test_user: User):
    """Test creating a post with empty title fails."""
    with pytest.raises(HTTPException) as exc_info:
        await create_post(title="   ", content="Test content", author=test_user)

    assert exc_info.value.status_code == 400
    assert "empty" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_create_post_empty_content(test_user: User):
    """Test creating a post with empty content fails."""
    with pytest.raises(HTTPException) as exc_info:
        await create_post(title="Test Post", content="   ", author=test_user)

    assert exc_info.value.status_code == 400
    assert "empty" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_get_post_by_id(test_user: User, test_post: Post):
    """Test getting a post by ID."""
    post = await get_post_by_id(test_post.id)

    assert post.id == test_post.id
    assert post.title == test_post.title
    assert post.author.id == test_user.id


@pytest.mark.asyncio
async def test_get_post_by_id_not_found():
    """Test getting a non-existent post returns 404."""
    with pytest.raises(HTTPException) as exc_info:
        await get_post_by_id(99999)

    assert exc_info.value.status_code == 404
    assert "not found" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_list_posts(test_user: User):
    """Test listing posts with pagination."""
    # Create multiple posts
    for i in range(5):
        await Post.create(
            title=f"Post {i}", content=f"Content {i}", author=test_user
        )

    posts, total = await list_posts(page=1, page_size=3)

    assert len(posts) == 3
    assert total == 5
    # Check ordering (newest first)
    assert posts[0].title == "Post 4"
    assert posts[2].title == "Post 2"


@pytest.mark.asyncio
async def test_list_posts_pagination():
    """Test pagination works correctly."""
    # Assuming some posts exist from previous tests
    posts, total = await list_posts(page=1, page_size=20)

    assert len(posts) <= 20
    assert total >= 0


@pytest.mark.asyncio
async def test_list_posts_invalid_page():
    """Test listing posts with invalid page fails."""
    with pytest.raises(HTTPException) as exc_info:
        await list_posts(page=0, page_size=20)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_list_posts_invalid_page_size():
    """Test listing posts with invalid page size fails."""
    with pytest.raises(HTTPException) as exc_info:
        await list_posts(page=1, page_size=100)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_update_post_by_author(test_user: User, test_post: Post):
    """Test author can update their post."""
    updated_post = await update_post(
        post_id=test_post.id,
        title="Updated Title",
        content="Updated content",
        current_user=test_user,
    )

    assert updated_post.id == test_post.id
    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Updated content"


@pytest.mark.asyncio
async def test_update_post_by_non_author(test_user: User, test_user2: User, test_post: Post):
    """Test non-author cannot update post."""
    with pytest.raises(HTTPException) as exc_info:
        await update_post(
            post_id=test_post.id,
            title="Hacked Title",
            content="Hacked content",
            current_user=test_user2,
        )

    assert exc_info.value.status_code == 403
    assert "author" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_update_post_not_found(test_user: User):
    """Test updating non-existent post fails."""
    with pytest.raises(HTTPException) as exc_info:
        await update_post(
            post_id=99999,
            title="Test",
            content="Test",
            current_user=test_user,
        )

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_post_by_author(test_user: User, test_post: Post):
    """Test author can delete their post."""
    post_id = test_post.id

    await delete_post(post_id=post_id, current_user=test_user)

    # Verify post is deleted
    deleted_post = await Post.filter(id=post_id).first()
    assert deleted_post is None


@pytest.mark.asyncio
async def test_delete_post_by_non_author(test_user: User, test_user2: User):
    """Test non-author cannot delete post."""
    # Create a post by test_user
    post = await Post.create(
        title="Test Post", content="Test content", author=test_user
    )

    with pytest.raises(HTTPException) as exc_info:
        await delete_post(post_id=post.id, current_user=test_user2)

    assert exc_info.value.status_code == 403
    assert "author" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_delete_post_not_found(test_user: User):
    """Test deleting non-existent post fails."""
    with pytest.raises(HTTPException) as exc_info:
        await delete_post(post_id=99999, current_user=test_user)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_check_post_author(test_user: User, test_user2: User, test_post: Post):
    """Test check_post_author helper function."""
    assert check_post_author(test_post, test_user) is True
    assert check_post_author(test_post, test_user2) is False

