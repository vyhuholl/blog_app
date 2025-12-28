"""
User-related Pydantic schemas for request/response validation.

This module defines schemas for user registration, login, and responses.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration request."""

    username: str = Field(..., min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    """Schema for user login request."""

    username: str
    password: str


class UserResponse(BaseModel):
    """Schema for authenticated user response (includes email)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    created_at: datetime


class UserPublic(BaseModel):
    """Schema for public user profile (no sensitive data)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    created_at: datetime

