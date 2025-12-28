# Data Model Specification

**Feature**: Blog Application Platform  
**Constitution Version**: 1.0.0  
**Date**: 2025-12-28

---

## Overview

This document defines the data model for the blog application platform using Tortoise ORM with SQLite. The model supports user authentication, blog post management, and commenting functionality.

---

## Database Configuration

### Technology
- **Database**: SQLite 3.x
- **ORM**: Tortoise ORM (async)
- **Migration Tool**: Alembic

### SQLite Settings
```python
# Enable Write-Ahead Logging for better concurrency
PRAGMA journal_mode=WAL;

# Enable foreign key constraints
PRAGMA foreign_keys=ON;
```

---

## Entity Relationship Diagram

```
┌─────────────┐
│    User     │
└─────────────┘
      │ 1
      │
      │ has many
      ├──────────────────┐
      │                  │
      │ *                │ *
┌─────────────┐    ┌─────────────┐
│    Post     │    │   Comment   │
└─────────────┘    └─────────────┘
      │ 1                │
      │                  │
      │ has many         │
      └──────────────────┘
               * belongs to
```

**Relationships**:
- User → Posts: One-to-Many (one user can create many posts)
- User → Comments: One-to-Many (one user can create many comments)
- Post → Comments: One-to-Many (one post can have many comments)

---

## Entities

### 1. User

**Purpose**: Represents a registered user account with authentication credentials.

**Tortoise ORM Model**:
```python
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class User(models.Model):
    """
    User model for authentication and authorship.
    """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=30, unique=True, index=True)
    email = fields.CharField(max_length=255, unique=True, index=True)
    password_hash = fields.CharField(max_length=255)  # bcrypt hash
    created_at = fields.DatetimeField(auto_now_add=True)
    
    # Relationships
    posts = fields.ReverseRelation["Post"]
    comments = fields.ReverseRelation["Comment"]
    
    class Meta:
        table = "users"
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.username
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique user identifier |
| `username` | String(30) | Unique, Not Null, Indexed | User's display name and login identifier |
| `email` | String(255) | Unique, Not Null, Indexed | User's email address for authentication |
| `password_hash` | String(255) | Not Null | bcrypt hashed password (never store plaintext) |
| `created_at` | Timestamp | Auto-generate | Account creation timestamp |

**Validation Rules**:
- `username`: 
  - Length: 3-30 characters
  - Pattern: Alphanumeric + underscores only (`^[a-zA-Z0-9_]+$`)
  - Must be unique (case-insensitive check in business logic)
- `email`:
  - Valid email format (RFC 5322)
  - Must be unique (case-insensitive check in business logic)
- `password` (before hashing):
  - Minimum length: 8 characters
  - No maximum (will be hashed to fixed length)

**Indexes**:
- Primary index on `id`
- Unique index on `username`
- Unique index on `email`
- Index on `created_at` for sorting

**Security Notes**:
- Password hashes stored using bcrypt with cost factor 12
- Never expose `password_hash` in API responses
- Implement rate limiting on authentication endpoints (future enhancement)

---

### 2. Post

**Purpose**: Represents a blog post with title, content, and authorship.

**Tortoise ORM Model**:
```python
class Post(models.Model):
    """
    Blog post model.
    """
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    content = fields.TextField()
    author = fields.ForeignKeyField(
        "models.User", 
        related_name="posts",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    # Relationships
    comments = fields.ReverseRelation["Comment"]
    
    class Meta:
        table = "posts"
        ordering = ["-created_at"]  # Newest first
    
    def __str__(self):
        return self.title
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique post identifier |
| `title` | String(200) | Not Null | Post title/headline |
| `content` | Text | Not Null | Post body content (plain text) |
| `author_id` | Integer | Foreign Key → User.id, Not Null, Indexed | Reference to post author |
| `created_at` | Timestamp | Auto-generate | Post creation timestamp |
| `updated_at` | Timestamp | Auto-update | Last modification timestamp |

**Validation Rules**:
- `title`:
  - Length: 1-200 characters
  - Cannot be only whitespace
- `content`:
  - Minimum length: 1 character
  - No maximum (TEXT field)
  - Cannot be only whitespace
- `author_id`:
  - Must reference valid User.id
  - Cannot be null

**Indexes**:
- Primary index on `id`
- Foreign key index on `author_id`
- Index on `created_at` for sorting and pagination
- Composite index on `(author_id, created_at)` for user's posts listing

**Relationships**:
- `author`: Foreign key to User (CASCADE delete - if user deleted, their posts are deleted)
- `comments`: Reverse relation to Comment (one post has many comments)

**Business Rules**:
- Only the post author can edit or delete the post
- Deleting a post cascades to delete all associated comments
- `updated_at` automatically updates on any modification

---

### 3. Comment

**Purpose**: Represents a user comment on a blog post.

**Tortoise ORM Model**:
```python
class Comment(models.Model):
    """
    Comment model for post discussions.
    """
    id = fields.IntField(pk=True)
    content = fields.CharField(max_length=1000)
    post = fields.ForeignKeyField(
        "models.Post",
        related_name="comments",
        on_delete=fields.CASCADE
    )
    author = fields.ForeignKeyField(
        "models.User",
        related_name="comments",
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "comments"
        ordering = ["created_at"]  # Oldest first
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
```

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | Integer | Primary Key, Auto-increment | Unique comment identifier |
| `content` | String(1000) | Not Null | Comment text content |
| `post_id` | Integer | Foreign Key → Post.id, Not Null, Indexed | Reference to parent post |
| `author_id` | Integer | Foreign Key → User.id, Not Null, Indexed | Reference to comment author |
| `created_at` | Timestamp | Auto-generate | Comment creation timestamp |
| `updated_at` | Timestamp | Auto-update | Last modification timestamp |

**Validation Rules**:
- `content`:
  - Length: 1-1000 characters
  - Cannot be only whitespace
- `post_id`:
  - Must reference valid Post.id
  - Cannot be null
- `author_id`:
  - Must reference valid User.id
  - Cannot be null

**Indexes**:
- Primary index on `id`
- Foreign key index on `post_id`
- Foreign key index on `author_id`
- Composite index on `(post_id, created_at)` for post's comments listing
- Index on `created_at` for sorting

**Relationships**:
- `post`: Foreign key to Post (CASCADE delete - if post deleted, comments are deleted)
- `author`: Foreign key to User (CASCADE delete - if user deleted, their comments are deleted)

**Business Rules**:
- Only the comment author can edit or delete their comment
- Comments belong to a single post (no comment threading/nesting)
- Comments are displayed chronologically (oldest first) under posts
- `updated_at` automatically updates on any modification

---

## Database Schema (SQL)

### Migration 001: Initial Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(30) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Posts table
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_posts_author_id ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at);
CREATE INDEX idx_posts_author_created ON posts(author_id, created_at);

-- Comments table
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content VARCHAR(1000) NOT NULL,
    post_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_author_id ON comments(author_id);
CREATE INDEX idx_comments_post_created ON comments(post_id, created_at);
CREATE INDEX idx_comments_created_at ON comments(created_at);
```

---

## Pydantic Schemas

### Request/Response Models

**User Schemas**:
```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# Request schemas
class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern="^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

# Response schemas
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        orm_mode = True

class UserPublic(BaseModel):
    id: int
    username: str
    created_at: datetime
    
    class Config:
        orm_mode = True
```

**Post Schemas**:
```python
# Request schemas
class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

class PostUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

# Response schemas
class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: UserPublic
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class PostList(BaseModel):
    id: int
    title: str
    author: UserPublic
    created_at: datetime
    
    class Config:
        orm_mode = True
```

**Comment Schemas**:
```python
# Request schemas
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

# Response schemas
class CommentResponse(BaseModel):
    id: int
    content: str
    author: UserPublic
    post_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

---

## Query Patterns & Optimization

### Common Queries

**Get posts with author (avoid N+1)**:
```python
posts = await Post.all().prefetch_related("author").order_by("-created_at")
```

**Get single post with author and comments**:
```python
post = await Post.get(id=post_id).prefetch_related("author", "comments__author")
```

**Get user's posts**:
```python
posts = await Post.filter(author_id=user_id).order_by("-created_at")
```

**Pagination**:
```python
page = 1
page_size = 20
offset = (page - 1) * page_size

posts = await Post.all().offset(offset).limit(page_size).prefetch_related("author")
total = await Post.all().count()
```

**Get comments for post**:
```python
comments = await Comment.filter(post_id=post_id).prefetch_related("author").order_by("created_at")
```

### Performance Considerations

1. **Always use prefetch_related/select_related** for foreign keys to avoid N+1 queries
2. **Implement pagination** for list endpoints (max 50 items per page)
3. **Use indexes** on frequently queried fields (author_id, created_at)
4. **Limit SELECT fields** when full object not needed (e.g., post list doesn't need content)
5. **Connection pooling** handled by Tortoise ORM automatically

---

## Data Validation Summary

### Field-Level Validation (Pydantic)
- **Username**: 3-30 chars, alphanumeric + underscore
- **Email**: Valid email format
- **Password**: Min 8 characters
- **Post Title**: 1-200 characters
- **Post Content**: Min 1 character
- **Comment Content**: 1-1000 characters

### Database-Level Constraints
- **Unique constraints**: username, email
- **Foreign key constraints**: author_id, post_id
- **Not null constraints**: All required fields
- **Cascade deletes**: Post deletion → comment deletion, User deletion → posts + comments deletion

### Business Logic Validation
- **Authorization**: Users can only edit/delete their own posts and comments
- **Existence checks**: Verify foreign key entities exist before creation
- **Whitespace validation**: Strip and check for empty strings

---

## Migration Strategy

### Alembic Configuration

**Initial setup**:
```bash
# Initialize Alembic
alembic init alembic

# Configure alembic.ini
# Set sqlalchemy.url = sqlite:///./blog.db

# Create first migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

**Future migrations**:
- All schema changes through Alembic migrations
- Never modify models without creating migration
- Test migrations on copy of production data before deploying
- Keep migrations in version control

---

## Testing Considerations

### Test Database
- Use separate SQLite file: `test_blog.db`
- Create/destroy for each test run
- Use pytest fixtures for database setup/teardown

### Test Data
- Factory pattern for creating test users, posts, comments
- Use faker library for realistic test data
- Ensure unique constraints respected in test data

### Example Fixture:
```python
import pytest
from tortoise.contrib.test import initializer, finalizer

@pytest.fixture(scope="module")
async def init_db():
    await initializer(["app.models"], db_url="sqlite://:memory:")
    yield
    await finalizer()

@pytest.fixture
async def test_user():
    user = await User.create(
        username="testuser",
        email="test@example.com",
        password_hash="$2b$12$..." # bcrypt hash
    )
    return user
```

---

## Security Considerations

### Password Storage
- **Never store plaintext passwords**
- Use bcrypt with cost factor 12
- Hash passwords in service layer before database operations
- Never expose password_hash in API responses or logs

### SQL Injection
- Tortoise ORM parameterizes all queries automatically
- Never use raw SQL without parameterization
- Validate all user input at Pydantic layer

### Authorization
- Verify user owns resource before allowing edit/delete
- Implement in service layer, not just API layer
- Use FastAPI dependencies for authentication checks

### Data Exposure
- Use separate Pydantic schemas for responses (exclude sensitive fields)
- Never return password_hash, even by accident
- Be careful with error messages (don't leak database structure)

---

## Next Steps

1. Implement Tortoise ORM models in `app/models/`
2. Create Alembic migrations for initial schema
3. Implement Pydantic schemas in `app/schemas/`
4. Set up database initialization in `app/main.py`
5. Implement query patterns in service layer

