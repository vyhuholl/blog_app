"""
Comment-related Pydantic schemas for request/response validation.

This module defines schemas for comment creation, updates, and responses.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.user import UserPublic


class CommentCreate(BaseModel):
    """Schema for comment creation request."""

    content: str = Field(..., min_length=1, max_length=1000)


class CommentUpdate(BaseModel):
    """Schema for comment update request."""

    content: str = Field(..., min_length=1, max_length=1000)


class CommentResponse(BaseModel):
    """Schema for comment response."""

    id: int
    content: str
    author: UserPublic
    post_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic configuration."""

        from_attributes = True

