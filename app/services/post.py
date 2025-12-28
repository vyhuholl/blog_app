"""
Post service layer.

This module provides business logic for post CRUD operations including
authorization checks, pagination, and database queries.
"""

from fastapi import HTTPException, status

from app.models.post import Post
from app.models.user import User


async def create_post(title: str, content: str, author: User) -> Post:
    """
    Create a new blog post.

    Args:
        title: Post title
        content: Post content
        author: User creating the post

    Returns:
        Created Post object with author prefetched

    Raises:
        HTTPException: If validation fails
    """
    # Validate title and content are not just whitespace
    if not title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty"
        )

    if not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty"
        )

    # Create post
    post = await Post.create(title=title.strip(), content=content.strip(), author=author)

    # Fetch with author for response
    await post.fetch_related("author")

    return post


async def get_post_by_id(post_id: int) -> Post:
    """
    Get a post by ID with author information.

    Args:
        post_id: ID of the post to retrieve

    Returns:
        Post object with author prefetched

    Raises:
        HTTPException: If post not found
    """
    post = await Post.filter(id=post_id).prefetch_related("author").first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    return post


async def list_posts(page: int = 1, page_size: int = 20) -> tuple[list[Post], int]:
    """
    List posts with pagination, ordered by created_at DESC.

    Args:
        page: Page number (1-indexed)
        page_size: Number of posts per page (max 50)

    Returns:
        Tuple of (list of Post objects, total count)

    Raises:
        HTTPException: If page or page_size are invalid
    """
    # Validate pagination parameters
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Page must be >= 1"
        )

    if page_size < 1 or page_size > 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Page size must be between 1 and 50",
        )

    # Calculate offset
    offset = (page - 1) * page_size

    # Get posts with author prefetched
    posts = (
        await Post.all()
        .prefetch_related("author")
        .order_by("-created_at")
        .offset(offset)
        .limit(page_size)
    )

    # Get total count
    total = await Post.all().count()

    return posts, total


async def update_post(post_id: int, title: str, content: str, current_user: User) -> Post:
    """
    Update a post (only by author).

    Args:
        post_id: ID of the post to update
        title: New title
        content: New content
        current_user: User attempting the update

    Returns:
        Updated Post object with author prefetched

    Raises:
        HTTPException: If post not found, user not authorized, or validation fails
    """
    # Get post
    post = await Post.filter(id=post_id).prefetch_related("author").first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check authorization
    if not check_post_author(post, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the post author can update this post",
        )

    # Validate title and content
    if not title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty"
        )

    if not content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Content cannot be empty"
        )

    # Update post
    post.title = title.strip()
    post.content = content.strip()
    await post.save()

    # Refresh to get updated_at
    await post.refresh_from_db()
    await post.fetch_related("author")

    return post


async def delete_post(post_id: int, current_user: User) -> None:
    """
    Delete a post (only by author). Cascade deletes comments.

    Args:
        post_id: ID of the post to delete
        current_user: User attempting the deletion

    Raises:
        HTTPException: If post not found or user not authorized
    """
    # Get post
    post = await Post.filter(id=post_id).prefetch_related("author").first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # Check authorization
    if not check_post_author(post, current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the post author can delete this post",
        )

    # Delete post (cascade deletes comments via on_delete=CASCADE)
    await post.delete()


def check_post_author(post: Post, user: User) -> bool:
    """
    Check if a user is the author of a post.

    Args:
        post: Post to check
        user: User to check

    Returns:
        True if user is the author, False otherwise
    """
    return post.author.id == user.id

