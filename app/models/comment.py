"""
Comment model for post discussions.

This module defines the Comment model with content, author and post relationships,
and timestamps.
"""

from tortoise import fields
from tortoise.models import Model


class Comment(Model):
    """
    Comment model for post discussions.

    Attributes:
        id: Primary key, auto-incremented integer
        content: Comment text content (1-1000 chars)
        post_id: Foreign key to Post.id
        author_id: Foreign key to User.id
        created_at: Timestamp of comment creation
        updated_at: Timestamp of last modification
    """

    id = fields.IntField(pk=True)
    content = fields.CharField(max_length=1000)
    post = fields.ForeignKeyField(
        "models.Post", related_name="comments", on_delete=fields.CASCADE
    )
    author = fields.ForeignKeyField(
        "models.User", related_name="comments", on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        """Model metadata."""

        table = "comments"
        ordering = ["created_at"]  # Oldest first

    def __str__(self) -> str:
        """String representation."""
        return f"Comment by {self.author_id} on {self.post_id}"

