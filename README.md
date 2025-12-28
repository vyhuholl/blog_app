# Blog Application Platform

A modern blog platform built with FastAPI, featuring user authentication, blog posts, and comments.

## Features

- **User Authentication**: Secure registration and login with JWT tokens and bcrypt password hashing
- **Blog Posts**: Create, read, update, and delete blog posts
- **Comments**: Add comments to posts with full CRUD operations
- **User Profiles**: Public user profiles showing post count and activity
- **Responsive Design**: Mobile-first design that works on all devices
- **RESTful API**: Clean API design with automatic OpenAPI documentation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Tortoise ORM** - Async ORM for database operations
- **SQLite** - Lightweight, file-based database
- **Alembic** - Database migration management
- **PyJWT** - JWT token authentication
- **bcrypt** - Secure password hashing
- **Uvicorn** - ASGI server

### Frontend
- **Jinja2** - Server-side templating
- **Vanilla JavaScript** - Progressive enhancement
- **CSS** - Custom styling with CSS variables

### Development
- **uv** - Fast Python package manager
- **pytest** - Testing framework
- **ruff** - Fast Python linter and formatter

## Quick Start

### Prerequisites

- Python 3.10+
- uv package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd blog_app
```

2. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set JWT_SECRET to a secure random value
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload
```

The application will be available at:
- Website: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- ReDoc Documentation: http://localhost:8000/redoc

## Project Structure

```
blog_app/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── models/                 # Tortoise ORM models
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/                 # API endpoints
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   ├── users.py
│   │   └── pages.py
│   ├── services/               # Business logic
│   │   ├── auth.py
│   │   ├── post.py
│   │   ├── comment.py
│   │   └── user.py
│   ├── dependencies/           # FastAPI dependencies
│   │   └── auth.py
│   └── templates/              # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── post_detail.html
│       ├── post_form.html
│       ├── login.html
│       ├── register.html
│       └── user_profile.html
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── tests/                      # Test files
├── alembic/                    # Database migrations
├── specs/                      # Design documents
└── README.md
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT token
- `POST /api/auth/logout` - Logout (clear cookie)
- `GET /api/auth/me` - Get current user information

### Posts
- `GET /api/posts` - List all posts (paginated)
- `POST /api/posts` - Create a new post (authenticated)
- `GET /api/posts/{id}` - Get a single post
- `PUT /api/posts/{id}` - Update a post (author only)
- `DELETE /api/posts/{id}` - Delete a post (author only)

### Comments
- `GET /api/posts/{post_id}/comments` - Get all comments for a post
- `POST /api/posts/{post_id}/comments` - Add a comment (authenticated)
- `PUT /api/comments/{id}` - Update a comment (author only)
- `DELETE /api/comments/{id}` - Delete a comment (author only)

### Users
- `GET /api/users/{id}` - Get user profile

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_posts_api.py
```

### Code Quality

```bash
# Run linter
ruff check .

# Format code
ruff format .

# Fix auto-fixable issues
ruff check --fix .
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=sqlite://./blog.db
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
BCRYPT_ROUNDS=12
ENVIRONMENT=development
```

**Important**: Generate a secure JWT secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Security Features

- **Password Hashing**: bcrypt with cost factor 12
- **JWT Tokens**: Stored in HTTP-only cookies for XSS protection
- **CORS**: Configured for localhost in development
- **Input Validation**: Pydantic schemas for all API inputs
- **SQL Injection Protection**: ORM-parameterized queries
- **Authorization**: Role-based access control for posts and comments

## Performance

- **Async Operations**: FastAPI + Tortoise ORM for non-blocking I/O
- **Database Optimization**: Proper indexes and eager loading
- **Pagination**: List endpoints support pagination (max 50 per page)
- **Gzip Compression**: Response compression middleware
- **Browser Caching**: Static assets cached for optimal performance

## Testing

The project includes comprehensive test coverage:

- **Unit Tests**: Service layer business logic (≥80% coverage)
- **Integration Tests**: API endpoint testing with TestClient
- **Database Tests**: In-memory SQLite for fast test execution

Run the test suite:
```bash
pytest --cov=app --cov-report=html
```

View coverage report: `htmlcov/index.html`

## Deployment

### Production Checklist

- [ ] Set `ENVIRONMENT=production` in .env
- [ ] Generate secure `JWT_SECRET`
- [ ] Enable HTTPS
- [ ] Set secure cookie flags (`secure=True`)
- [ ] Configure CORS for your domain
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Enable rate limiting (future enhancement)

### Production Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install uv
COPY requirements.txt .
RUN uv pip install --system -r requirements.txt
COPY . .
CMD alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Documentation

- **API Documentation**: Visit `/docs` for interactive Swagger UI
- **ReDoc Documentation**: Visit `/redoc` for clean API reference
- **OpenAPI Specification**: Available at `/openapi.json`
- **Design Documents**: See `specs/001-blog-app/` for detailed planning docs

## Contributing

1. Follow PEP 8 style guidelines (enforced by ruff)
2. Write tests for new features
3. Maintain ≥80% code coverage for business logic
4. Update documentation for API changes
5. Use conventional commit messages

## License

This project is part of a learning exercise. Use at your own risk.

## Support

For issues, questions, or contributions, please refer to the design documents in the `specs/` directory.

---

**Built with ❤️ using FastAPI and modern Python tools**
