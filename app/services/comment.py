"""
Comment service layer.

This module provides business logic for comment CRUD operations including
authorization checks and database queries.
"""

from fastapi import HTTPException, status

from app.models.comment import Comment
from app.models.post import Post
from app.models.user import User


async def create_comment(post_id: int, content: str, author: User) -> Comment:
    """
    Create a new comment on a post.

    Args:
        post_id: ID of the post to comment on
        content: Comment content
        author: User creating the comment

    Returns:
        Created Comment object with author prefetched

    Raises:
        HTTPException: If post not found or validation fails
    """
    # Validate content is not just whitespace
    if not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty"
        )

    # Check if post exists
    post = await Post.filter(id=post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Create comment
    comment = await Comment.create(content=content.strip(), post=post, author=author)

    # Fetch with author for response
    await comment.fetch_related("author")

    return comment


async def get_comments_by_post(post_id: int) -> list[Comment]:
    """
    Get all comments for a post, ordered chronologically (oldest first).

    Args:
        post_id: ID of the post

    Returns:
        List of Comment objects with authors prefetched
    """
    comments = (
        await Comment.filter(post_id=post_id)
        .prefetch_related("author")
        .order_by("created_at")
    )

    return comments


async def update_comment(comment_id: int, content: str, current_user: User) -> Comment:
    """
    Update a comment (only by author).

    Args:
        comment_id: ID of the comment to update
        content: New content
        current_user: User attempting the update

    Returns:
        Updated Comment object with author prefetched

    Raises:
        HTTPException: If comment not found, user not authorized, or validation fails
    """
    # Get comment
    comment = await Comment.filter(id=comment_id).prefetch_related("author").first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Check authorization
    if not check_comment_author(comment, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the comment author can update this comment",
        )

    # Validate content
    if not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty"
        )

    # Update comment
    comment.content = content.strip()
    await comment.save()

    # Refresh to get updated_at
    await comment.refresh_from_db()
    await comment.fetch_related("author")

    return comment


async def delete_comment(comment_id: int, current_user: User) -> None:
    """
    Delete a comment (only by author).

    Args:
        comment_id: ID of the comment to delete
        current_user: User attempting the deletion

    Raises:
        HTTPException: If comment not found or user not authorized
    """
    # Get comment
    comment = await Comment.filter(id=comment_id).prefetch_related("author").first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Check authorization
    if not check_comment_author(comment, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the comment author can delete this comment",
        )

    # Delete comment
    await comment.delete()


def check_comment_author(comment: Comment, user: User) -> bool:
    """
    Check if a user is the author of a comment.

    Args:
        comment: Comment to check
        user: User to check

    Returns:
        True if user is the author, False otherwise
    """
    return comment.author.id == user.id

