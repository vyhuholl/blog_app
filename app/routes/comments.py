"""
Comment-related API endpoints.

This module provides RESTful API routes for comment CRUD operations.
"""

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse, CommentUpdate
from app.services.comment import (
    create_comment,
    delete_comment,
    get_comments_by_post,
    update_comment,
)

router = APIRouter(prefix="/api", tags=["comments"])


@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse])
async def get_post_comments(post_id: int):
    """
    Get all comments for a post.

    Args:
        post_id: ID of the post

    Returns:
        List of comments
    """
    comments = await get_comments_by_post(post_id)
    return comments


@router.post(
    "/posts/{post_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post_comment(
    post_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
):
    """
    Create a new comment on a post (requires authentication).

    Args:
        post_id: ID of the post to comment on
        comment_data: Comment creation data
        current_user: Authenticated user (from dependency)

    Returns:
        Created comment
    """
    comment = await create_comment(
        post_id=post_id, content=comment_data.content, author=current_user
    )

    return comment


@router.put("/comments/{comment_id}", response_model=CommentResponse)
async def update_existing_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_user),
):
    """
    Update a comment (requires authentication, author only).

    Args:
        comment_id: ID of the comment to update
        comment_data: Updated comment data
        current_user: Authenticated user (from dependency)

    Returns:
        Updated comment
    """
    comment = await update_comment(
        comment_id=comment_id, content=comment_data.content, current_user=current_user
    )

    return comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_comment(
    comment_id: int, current_user: User = Depends(get_current_user)
):
    """
    Delete a comment (requires authentication, author only).

    Args:
        comment_id: ID of the comment to delete
        current_user: Authenticated user (from dependency)

    Returns:
        No content (204)
    """
    await delete_comment(comment_id=comment_id, current_user=current_user)

