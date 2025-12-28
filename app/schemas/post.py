"""
Post-related Pydantic schemas for request/response validation.

This module defines schemas for post creation, updates, and responses.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.user import UserPublic


class PostCreate(BaseModel):
    """Schema for post creation request."""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PostUpdate(BaseModel):
    """Schema for post update request."""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PostResponse(BaseModel):
    """Schema for full post response (includes content)."""

    id: int
    title: str
    content: str
    author: UserPublic
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class PostList(BaseModel):
    """Schema for post list item (excludes content for performance)."""

    id: int
    title: str
    author: UserPublic
    created_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class PostListResponse(BaseModel):
    """Schema for paginated post list response."""

    items: list[PostList]
    total: int
    page: int
    page_size: int
    total_pages: int

