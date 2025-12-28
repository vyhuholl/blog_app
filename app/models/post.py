"""
Post model for blog posts.

This module defines the Post model with title, content, author relationship,
and timestamps.
"""

from tortoise import fields
from tortoise.models import Model


class Post(Model):
    """
    Blog post model.

    Attributes:
        id: Primary key, auto-incremented integer
        title: Post title (1-200 chars)
        content: Post body content (TEXT field, no max length)
        author_id: Foreign key to User.id
        created_at: Timestamp of post creation
        updated_at: Timestamp of last modification
        comments: Reverse relation to Comment model
    """

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author = fields.ForeignKeyField(
        "models.User", related_name="posts", on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # Reverse relation (defined by ForeignKey in Comment model)
    # comments: fields.ReverseRelation["Comment"]

    class Meta:
        """Model metadata."""

        table = "posts"
        ordering = ["-created_at"]  # Newest first

    def __str__(self) -> str:
        """String representation."""
        return self.title

