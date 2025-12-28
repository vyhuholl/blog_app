"""
User model for authentication and authorship.

This module defines the User model with authentication-related fields
and relationships to posts and comments.
"""

from tortoise import fields
from tortoise.models import Model


class User(Model):
    """
    User model for authentication and authorship.

    Attributes:
        id: Primary key, auto-incremented integer
        username: Unique username (3-30 chars, alphanumeric + underscore)
        email: Unique email address
        password_hash: bcrypt hashed password (never store plaintext)
        created_at: Timestamp of account creation
        posts: Reverse relation to Post model
        comments: Reverse relation to Comment model
    """

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    password_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)

    # Reverse relations (defined by ForeignKey in other models)
    # posts: fields.ReverseRelation["Post"]
    # comments: fields.ReverseRelation["Comment"]

    class Meta:
        """Model metadata."""

        table = "users"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """String representation."""
        return self.username

