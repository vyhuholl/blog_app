"""Initial schema migration.

Revision ID: 001
Create Date: 2025-12-28

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Create initial schema with users, posts, and comments tables."""
    # Users table
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(30) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at)")

    # Posts table
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(200) NOT NULL,
            content TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS idx_posts_author_id ON posts(author_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_posts_author_created ON posts(author_id, created_at)"
    )

    # Comments table
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content VARCHAR(1000) NOT NULL,
            post_id INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """
    )

    op.execute("CREATE INDEX IF NOT EXISTS idx_comments_post_id ON comments(post_id)")
    op.execute("CREATE INDEX IF NOT EXISTS idx_comments_author_id ON comments(author_id)")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_comments_post_created ON comments(post_id, created_at)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_comments_created_at ON comments(created_at)"
    )

    # Enable WAL mode for better concurrency
    op.execute("PRAGMA journal_mode=WAL")
    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    """Drop all tables."""
    op.execute("DROP TABLE IF EXISTS comments")
    op.execute("DROP TABLE IF EXISTS posts")
    op.execute("DROP TABLE IF EXISTS users")

