"""
Post-related API endpoints.

This module provides RESTful API routes for blog post CRUD operations.
"""

from math import ceil

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.post import PostCreate, PostListResponse, PostResponse, PostUpdate
from app.services.post import (
    create_post,
    delete_post,
    get_post_by_id,
    list_posts,
    update_post,
)

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.get("", response_model=PostListResponse)
async def get_posts(page: int = 1, page_size: int = 20):
    """
    List blog posts with pagination.

    Args:
        page: Page number (default: 1)
        page_size: Items per page (default: 20, max: 50)

    Returns:
        Paginated list of posts
    """
    posts, total = await list_posts(page=page, page_size=page_size)

    total_pages = ceil(total / page_size) if total > 0 else 0

    return PostListResponse(
        items=posts, total=total, page=page, page_size=page_size, total_pages=total_pages
    )


@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_new_post(
    post_data: PostCreate, current_user: User = Depends(get_current_user)
):
    """
    Create a new blog post (requires authentication).

    Args:
        post_data: Post creation data
        current_user: Authenticated user (from dependency)

    Returns:
        Created post
    """
    post = await create_post(
        title=post_data.title, content=post_data.content, author=current_user
    )

    return post


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """
    Get a single post by ID.

    Args:
        post_id: ID of the post

    Returns:
        Post details
    """
    post = await get_post_by_id(post_id)
    return post


@router.put("/{post_id}", response_model=PostResponse)
async def update_existing_post(
    post_id: int,
    post_data: PostUpdate,
    current_user: User = Depends(get_current_user),
):
    """
    Update a post (requires authentication, author only).

    Args:
        post_id: ID of the post to update
        post_data: Updated post data
        current_user: Authenticated user (from dependency)

    Returns:
        Updated post
    """
    post = await update_post(
        post_id=post_id,
        title=post_data.title,
        content=post_data.content,
        current_user=current_user,
    )

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_post(
    post_id: int, current_user: User = Depends(get_current_user)
):
    """
    Delete a post (requires authentication, author only).

    Args:
        post_id: ID of the post to delete
        current_user: Authenticated user (from dependency)

    Returns:
        No content (204)
    """
    await delete_post(post_id=post_id, current_user=current_user)

