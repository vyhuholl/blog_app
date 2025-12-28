"""
Unit tests for comment service layer.
"""

import pytest
from fastapi import HTTPException

from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User
from app.services.comment import (
    check_comment_author,
    create_comment,
    delete_comment,
    get_comments_by_post,
    update_comment,
)


@pytest.mark.asyncio
async def test_create_comment(test_post: Post, test_user: User):
    """Test creating a comment."""
    comment = await create_comment(
        post_id=test_post.id, content="Great post!", author=test_user
    )

    assert comment.content == "Great post!"
    assert comment.post_id == test_post.id
    assert comment.author.id == test_user.id
    assert comment.id is not None


@pytest.mark.asyncio
async def test_create_comment_empty_content(test_post: Post, test_user: User):
    """Test creating a comment with empty content fails."""
    with pytest.raises(HTTPException) as exc_info:
        await create_comment(post_id=test_post.id, content="   ", author=test_user)

    assert exc_info.value.status_code == 400
    assert "empty" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_create_comment_on_nonexistent_post(test_user: User):
    """Test creating a comment on non-existent post fails."""
    with pytest.raises(HTTPException) as exc_info:
        await create_comment(post_id=99999, content="Test comment", author=test_user)

    assert exc_info.value.status_code == 404
    assert "post not found" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_get_comments_by_post(test_post: Post, test_user: User, test_user2: User):
    """Test getting comments for a post."""
    # Create multiple comments
    await Comment.create(content="First comment", post=test_post, author=test_user)
    await Comment.create(content="Second comment", post=test_post, author=test_user2)
    await Comment.create(content="Third comment", post=test_post, author=test_user)

    comments = await get_comments_by_post(test_post.id)

    assert len(comments) >= 3
    # Check ordering (oldest first)
    assert comments[0].content == "First comment"
    assert comments[1].content == "Second comment"


@pytest.mark.asyncio
async def test_get_comments_by_post_empty(test_post: Post):
    """Test getting comments for a post with no comments."""
    comments = await get_comments_by_post(test_post.id)

    assert len(comments) == 0


@pytest.mark.asyncio
async def test_update_comment_by_author(test_user: User, test_post: Post):
    """Test author can update their comment."""
    comment = await Comment.create(
        content="Original content", post=test_post, author=test_user
    )

    updated_comment = await update_comment(
        comment_id=comment.id, content="Updated content", current_user=test_user
    )

    assert updated_comment.id == comment.id
    assert updated_comment.content == "Updated content"


@pytest.mark.asyncio
async def test_update_comment_by_non_author(
    test_user: User, test_user2: User, test_post: Post
):
    """Test non-author cannot update comment."""
    comment = await Comment.create(
        content="Original content", post=test_post, author=test_user
    )

    with pytest.raises(HTTPException) as exc_info:
        await update_comment(
            comment_id=comment.id, content="Hacked content", current_user=test_user2
        )

    assert exc_info.value.status_code == 403
    assert "author" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_update_comment_not_found(test_user: User):
    """Test updating non-existent comment fails."""
    with pytest.raises(HTTPException) as exc_info:
        await update_comment(comment_id=99999, content="Test", current_user=test_user)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_comment_by_author(test_user: User, test_post: Post):
    """Test author can delete their comment."""
    comment = await Comment.create(content="Test comment", post=test_post, author=test_user)
    comment_id = comment.id

    await delete_comment(comment_id=comment_id, current_user=test_user)

    # Verify comment is deleted
    deleted_comment = await Comment.filter(id=comment_id).first()
    assert deleted_comment is None


@pytest.mark.asyncio
async def test_delete_comment_by_non_author(
    test_user: User, test_user2: User, test_post: Post
):
    """Test non-author cannot delete comment."""
    comment = await Comment.create(content="Test comment", post=test_post, author=test_user)

    with pytest.raises(HTTPException) as exc_info:
        await delete_comment(comment_id=comment.id, current_user=test_user2)

    assert exc_info.value.status_code == 403
    assert "author" in exc_info.value.detail.lower()


@pytest.mark.asyncio
async def test_delete_comment_not_found(test_user: User):
    """Test deleting non-existent comment fails."""
    with pytest.raises(HTTPException) as exc_info:
        await delete_comment(comment_id=99999, current_user=test_user)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_check_comment_author(test_user: User, test_user2: User, test_post: Post):
    """Test check_comment_author helper function."""
    comment = await Comment.create(content="Test", post=test_post, author=test_user)

    assert check_comment_author(comment, test_user) is True
    assert check_comment_author(comment, test_user2) is False

