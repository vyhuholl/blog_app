# Quickstart Guide: Blog Application Platform

**Feature**: Blog Application Platform  
**Constitution Version**: 1.0.0  
**Date**: 2025-12-28

---

## Overview

This guide will help you set up and run the blog application platform on your local machine for development purposes.

**Tech Stack**:
- Backend: FastAPI (Python 3.10+)
- Database: SQLite with Tortoise ORM
- Frontend: Jinja2 templates with vanilla HTML/CSS/JavaScript
- Testing: pytest
- Package Manager: uv

---

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **uv**: Fast Python package manager
- **Git**: For version control
- **Operating System**: macOS, Linux, or Windows with WSL

### Install uv (if not already installed)

**macOS/Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell)**:
```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

**Alternative (via pip)**:
```bash
pip install uv
```

Verify installation:
```bash
uv --version
```

---

## Quick Setup (5 minutes)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd blog_app
```

### 2. Create Virtual Environment
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

Example `.env` file:
```env
DATABASE_URL=sqlite://./blog.db
JWT_SECRET=your-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
BCRYPT_ROUNDS=12
ENVIRONMENT=development
```

**Generate a secure JWT secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Initialize Database
```bash
# Run Alembic migrations
alembic upgrade head
```

### 6. Run Development Server
```bash
uvicorn app.main:app --reload
```

The application will be available at:
- **Website**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

---

## Project Structure

```
blog_app/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/                 # Tortoise ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   └── users.py
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── dependencies/           # FastAPI dependencies
│   │   ├── __init__.py
│   │   └── auth.py
│   └── templates/              # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── post.html
│       ├── post_form.html
│       ├── login.html
│       └── register.html
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── tests/                      # Test files
│   ├── __init__.py
│   ├── conftest.py             # pytest fixtures
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_comments.py
│   └── test_users.py
├── alembic/                    # Database migrations
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── specs/                      # Design documents
│   └── 001-blog-app/
│       ├── spec.md
│       ├── plan.md
│       ├── research.md
│       ├── data-model.md
│       └── contracts/
├── pyproject.toml              # Project configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore
└── README.md
```

---

## Development Workflow

### Running the Application

**Development mode (auto-reload)**:
```bash
uvicorn app.main:app --reload --log-level debug
```

**Production mode**:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Database Migrations

**Create a new migration**:
```bash
alembic revision --autogenerate -m "Description of changes"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback last migration**:
```bash
alembic downgrade -1
```

**View migration history**:
```bash
alembic history
```

### Running Tests

**Run all tests**:
```bash
pytest
```

**Run with coverage**:
```bash
pytest --cov=app --cov-report=html --cov-report=term
```

**Run specific test file**:
```bash
pytest tests/test_auth.py
```

**Run specific test**:
```bash
pytest tests/test_auth.py::test_user_registration
```

**Run tests matching pattern**:
```bash
pytest -k "test_post"
```

### Code Quality

**Lint and format code**:
```bash
ruff check .
ruff format .
```

**Fix auto-fixable issues**:
```bash
ruff check --fix .
```

**Type checking (if using mypy)**:
```bash
mypy app/
```

---

## Common Development Tasks

### Creating a New User (via API)

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
  }' \
  -c cookies.txt
```

### Creating a Post

```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first blog post."
  }'
```

### Listing Posts

```bash
curl http://localhost:8000/api/posts?page=1&page_size=20
```

### Adding a Comment

```bash
curl -X POST http://localhost:8000/api/posts/1/comments \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "content": "Great post!"
  }'
```

---

## Troubleshooting

### Port Already in Use

If port 8000 is already in use, specify a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Database Locked Error

SQLite can experience lock issues with concurrent access. If you encounter this:

1. Ensure WAL mode is enabled (should be automatic in config)
2. Close any other database connections
3. Check for zombie processes: `ps aux | grep uvicorn`
4. Delete `blog.db-shm` and `blog.db-wal` if they exist

### Migration Issues

**Reset database (development only)**:
```bash
# Backup data first!
rm blog.db
alembic upgrade head
```

**Check current migration status**:
```bash
alembic current
```

### Import Errors

If you encounter import errors:
```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Reinstall dependencies
uv pip install -r requirements.txt

# Verify Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### JWT Token Issues

If authentication isn't working:
1. Verify `JWT_SECRET` is set in `.env`
2. Check cookie settings in browser DevTools (should see `access_token`)
3. Ensure `credentials: 'include'` is set in fetch requests
4. Check browser console for CORS errors

---

## API Documentation

### Interactive API Docs

FastAPI automatically generates interactive documentation:

**Swagger UI** (http://localhost:8000/docs):
- Test all API endpoints
- See request/response schemas
- Authenticate and try protected endpoints

**ReDoc** (http://localhost:8000/redoc):
- Clean, readable API documentation
- Better for reference than testing

### OpenAPI Specification

The complete API specification is available at:
- **JSON**: http://localhost:8000/openapi.json
- **YAML**: `specs/001-blog-app/contracts/openapi.yaml`

---

## Testing Strategy

### Test Database

Tests use an in-memory SQLite database for speed:
```python
# tests/conftest.py
@pytest.fixture(scope="module")
async def init_db():
    await initializer(
        modules=["app.models"],
        db_url="sqlite://:memory:"
    )
    yield
    await finalizer()
```

### Test Organization

```
tests/
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
│   ├── test_user_registration
│   ├── test_user_login
│   ├── test_user_logout
│   └── test_get_current_user
├── test_posts.py         # Post CRUD tests
│   ├── test_create_post
│   ├── test_list_posts
│   ├── test_get_post
│   ├── test_update_post
│   └── test_delete_post
├── test_comments.py      # Comment CRUD tests
│   ├── test_create_comment
│   ├── test_list_comments
│   ├── test_update_comment
│   └── test_delete_comment
└── test_users.py         # User profile tests
    └── test_get_user_profile
```

### Coverage Goals

- **Business Logic**: ≥80% coverage
- **API Endpoints**: 100% of routes tested
- **Critical Paths**: User registration, login, post creation, commenting

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite://./blog.db` | Database connection string |
| `JWT_SECRET` | (required) | Secret key for JWT signing |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRE_MINUTES` | `1440` | Token expiration (24 hours) |
| `BCRYPT_ROUNDS` | `12` | bcrypt cost factor |
| `ENVIRONMENT` | `development` | Environment name |

### FastAPI Configuration

See `app/config.py` for application configuration:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440
    bcrypt_rounds: int = 12
    environment: str = "development"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## Performance Optimization

### Database Optimization

1. **Enable WAL mode** (automatically configured):
   ```sql
   PRAGMA journal_mode=WAL;
   ```

2. **Use indexes** (defined in models):
   - `users.username`
   - `users.email`
   - `posts.author_id`
   - `posts.created_at`
   - `comments.post_id`

3. **Eager loading** (avoid N+1 queries):
   ```python
   posts = await Post.all().prefetch_related("author")
   ```

### API Performance

1. **Pagination**: Limit 50 items per page
2. **Async/Await**: All database operations are async
3. **Connection Pooling**: Managed by Tortoise ORM
4. **Response Compression**: Gzip middleware enabled

### Frontend Performance

1. **CSS**: Single minified file (~10KB)
2. **JavaScript**: Minimal, only for enhancement (~10KB)
3. **Browser Caching**: Static assets cached for 1 year
4. **No External Dependencies**: No CDN requests

---

## Deployment Considerations

### Production Checklist

- [ ] Change `JWT_SECRET` to a secure random value
- [ ] Set `ENVIRONMENT=production`
- [ ] Enable HTTPS
- [ ] Set secure cookie flags (`secure=True`)
- [ ] Configure CORS for your domain
- [ ] Set up database backups
- [ ] Configure logging (file + monitoring service)
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Enable rate limiting (future enhancement)
- [ ] Review and harden security settings

### Example Production Command

```bash
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level info \
  --no-access-log
```

### Systemd Service Example

```ini
[Unit]
Description=Blog Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/blog_app
Environment="PATH=/var/www/blog_app/.venv/bin"
ExecStart=/var/www/blog_app/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always

[Install]
WantedBy=multi-user.target
```

### Docker Example (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy dependency files
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy application
COPY . .

# Run migrations and start server
CMD alembic upgrade head && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Next Steps

1. **Implement Models**: Create Tortoise ORM models in `app/models/`
2. **Implement Schemas**: Create Pydantic schemas in `app/schemas/`
3. **Implement Services**: Business logic in `app/services/`
4. **Implement Routes**: API endpoints in `app/routes/`
5. **Create Templates**: Jinja2 templates in `app/templates/`
6. **Write Tests**: Comprehensive tests in `tests/`
7. **Add Styling**: CSS in `static/css/style.css`
8. **Add Interactivity**: JavaScript in `static/js/main.js`

---

## Resources

### Documentation
- **FastAPI**: https://fastapi.tiangolo.com/
- **Tortoise ORM**: https://tortoise.github.io/
- **Alembic**: https://alembic.sqlalchemy.org/
- **pytest**: https://docs.pytest.org/
- **uv**: https://github.com/astral-sh/uv

### API Testing
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Spec**: `specs/001-blog-app/contracts/openapi.yaml`

### Design Documents
- **Feature Spec**: `specs/001-blog-app/spec.md`
- **Implementation Plan**: `specs/001-blog-app/plan.md`
- **Technical Research**: `specs/001-blog-app/research.md`
- **Data Model**: `specs/001-blog-app/data-model.md`

---

## Getting Help

### Common Issues
1. Check the Troubleshooting section above
2. Review application logs for error details
3. Verify environment configuration (`.env`)
4. Ensure all dependencies are installed (`uv pip list`)

### Development Tips
- Use API docs (Swagger UI) to test endpoints
- Check browser DevTools for frontend errors
- Use `pytest -v` for verbose test output
- Enable debug logging for detailed information

### Need Support?
- Review design documents in `specs/001-blog-app/`
- Check API contracts in `specs/001-blog-app/contracts/`
- Refer to constitutional principles in `.specify/memory/constitution.md`

---

**Happy Coding! 🚀**

