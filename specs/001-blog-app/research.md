# Technical Research & Decisions

**Feature**: Blog Application Platform  
**Constitution Version**: 1.0.0  
**Date**: 2025-12-28

---

## Overview

This document consolidates technical research and decisions for the blog application platform. All technology choices prioritize minimal dependencies, maintainability, and alignment with constitutional principles.

---

## Backend Framework

### Decision
**FastAPI** - Modern Python web framework

### Rationale
- **Performance**: Built on Starlette and Pydantic, provides high performance with async/await support
- **Developer Experience**: Automatic OpenAPI documentation generation, type hints throughout, excellent error messages
- **Modern Python**: Leverages Python 3.7+ features (type hints, async/await)
- **Minimal Boilerplate**: Concise route definitions, automatic request validation via Pydantic models
- **Testing-Friendly**: Easy dependency injection, excellent test client support
- **Active Ecosystem**: Well-maintained, large community, excellent documentation

### Alternatives Considered
- **Flask**: More mature but lacks native async support, requires more manual setup for validation/documentation
- **Django**: Too heavyweight for this use case, brings many features (admin, migrations, ORM) not needed
- **Starlette**: FastAPI is built on it but adds validation/documentation—no reason to drop down a level

### Implementation Notes
- Use Pydantic models for request/response validation
- Leverage dependency injection for database sessions, authentication
- Structure: `app/` directory with `main.py`, `routes/`, `models/`, `services/`, `schemas/`

---

## Database & ORM

### Decision
**SQLite** (database) + **Tortoise ORM** (ORM) + **Alembic** (migrations)

### Rationale

**SQLite**:
- **Simplicity**: Single file database, no separate server process required
- **Production-Ready**: Suitable for small-to-medium traffic blogs (thousands of users, millions of posts)
- **Zero Configuration**: No installation, connection pooling, or server management
- **ACID Compliant**: Full transaction support, data integrity guarantees
- **Performance**: Fast for read-heavy workloads typical of blogs

**Tortoise ORM**:
- **Async Native**: Built for async/await, integrates perfectly with FastAPI
- **Django-Like API**: Familiar patterns for Python developers (similar to Django ORM)
- **Type Safety**: Excellent type hint support, IDE autocomplete
- **Minimal Magic**: Straightforward query API, clear relationship definitions
- **Alembic Integration**: Works with Alembic for migrations

**Alembic**:
- **Industry Standard**: SQLAlchemy's migration tool, battle-tested
- **Tortoise Compatible**: Can work with Tortoise ORM via aerich or direct schema inspection
- **Version Control**: Migrations as code, trackable in git
- **Rollback Support**: Safe schema evolution with up/down migrations

### Alternatives Considered
- **PostgreSQL**: Overkill for initial deployment, adds infrastructure complexity
- **SQLAlchemy ORM**: Not async-native, requires async extensions (asyncio, aiosqlite)
- **Raw SQL**: No abstraction benefits, more boilerplate, less type safety
- **Peewee**: Simpler but lacks async support and active maintenance

### Implementation Notes
- Database file: `blog.db` in project root (configurable via environment)
- Use Tortoise ORM models inheriting from `Model` class
- Alembic for migration management: `alembic init`, migration scripts in `alembic/versions/`
- Enable WAL mode for better concurrency: `PRAGMA journal_mode=WAL`
- Proper foreign key constraints with cascading deletes

---

## Authentication

### Decision
**JWT tokens** (via PyJWT) with **HTTP-only cookies**

### Rationale

**JWT (JSON Web Tokens)**:
- **Stateless**: No server-side session storage required
- **Self-Contained**: Token carries user identity and claims
- **Performance**: No database lookups for authentication (only for authorization if needed)
- **Standard**: Industry-standard format (RFC 7519)

**PyJWT Library**:
- **Minimal**: Single-purpose library, no bloat
- **Well-Maintained**: Active development, security updates
- **Flexible**: Supports multiple algorithms (HS256, RS256)

**HTTP-only Cookies** (vs localStorage/sessionStorage):
- **Security**: Protected from XSS attacks (JavaScript cannot access)
- **Automatic**: Browser sends with every request
- **Refresh Pattern**: Easy to implement refresh token rotation

**bcrypt for Password Hashing**:
- **Industry Standard**: Recommended by OWASP, NIST
- **Adaptive**: Configurable work factor (cost factor) for future-proofing
- **Salt Built-In**: Automatic per-password salting
- **Slow by Design**: Resistant to brute-force attacks

### Alternatives Considered
- **Session-Based Auth**: Requires server-side storage (Redis/database), adds complexity
- **OAuth/Social Login**: Out of scope, adds dependency on external providers
- **argon2**: More modern than bcrypt but less widespread Python support
- **Bearer Token in Header**: Requires client-side storage, less secure than HTTP-only cookies

### Implementation Notes
- JWT secret key in environment variable (`JWT_SECRET`)
- Token expiration: 24 hours (configurable)
- Refresh token: 7 days (configurable)
- bcrypt rounds: 12 (balance of security and performance)
- Cookie settings: `httponly=True`, `secure=True` (production), `samesite='lax'`

---

## Frontend Approach

### Decision
**Jinja2** templates + **vanilla HTML/CSS/JavaScript**

### Rationale

**Server-Side Rendering (Jinja2)**:
- **SEO-Friendly**: Content available on initial page load
- **Performance**: Faster initial paint than client-side rendering
- **Simplicity**: No build process, no transpilation
- **FastAPI Native**: Jinja2 support built into FastAPI

**Vanilla HTML/CSS/JavaScript**:
- **Zero Dependencies**: No npm, webpack, React/Vue/Angular
- **Minimal Bundle Size**: Only custom code, no framework overhead
- **Progressive Enhancement**: Works without JavaScript, enhances with it
- **Full Control**: No framework abstractions, direct DOM manipulation
- **Long-Term Stability**: No framework version upgrades, breaking changes

### Alternatives Considered
- **React/Vue/Svelte**: Overkill for blog app, requires build process, large bundle sizes
- **HTMX**: Interesting but adds dependency, requires learning new patterns
- **Alpine.js**: Lightweight but still a dependency, not needed for simple interactivity
- **Tailwind CSS**: Utility-first CSS is great but adds build step, bloats HTML

### Implementation Notes
- Templates in `templates/` directory: `base.html`, `index.html`, `post.html`, etc.
- CSS structure: Single `style.css` file with CSS custom properties for theming
- JavaScript: Progressive enhancement for form validation, async operations
- Responsive design: Mobile-first CSS with media queries
- Accessibility: Semantic HTML5, ARIA labels where needed, keyboard navigation

---

## Development Tools

### Decision
**uv** (package management) + **pytest** (testing) + **ruff** (linting)

### Rationale

**uv**:
- **Speed**: 10-100x faster than pip, written in Rust
- **Modern**: Unified interface for venv, pip, pip-tools
- **Deterministic**: Lock file support for reproducible builds
- **Actively Developed**: By Astral (creators of ruff)

**pytest**:
- **Industry Standard**: Most popular Python testing framework
- **Rich Ecosystem**: Plugins for coverage, async, fixtures
- **Readable**: Simple assertion syntax, clear output
- **FastAPI Integration**: Excellent test client support

**ruff**:
- **Speed**: 10-100x faster than flake8/pylint, written in Rust
- **All-in-One**: Replaces flake8, isort, pyupgrade, black
- **Configurable**: Extensive rule set, easy to configure
- **Modern**: Active development, rapid feature additions

### Alternatives Considered
- **poetry/pipenv**: More complex than needed, uv is faster and simpler
- **unittest**: Less flexible than pytest, more boilerplate
- **black**: Opinionated formatter, ruff includes formatting capabilities
- **flake8/pylint**: Slower, multiple tools needed, ruff consolidates

### Implementation Notes
- `pyproject.toml` for configuration (uv, ruff, pytest)
- `requirements.txt` generated by uv for production dependencies
- Test structure: `tests/` directory with `test_*.py` files
- Coverage target: ≥80% for business logic
- Pre-commit hooks: ruff for linting/formatting

---

## Web Server

### Decision
**Uvicorn** (ASGI server)

### Rationale
- **FastAPI Native**: Recommended by FastAPI documentation
- **Performance**: Fast ASGI implementation using uvloop and httptools
- **Development Friendly**: Auto-reload during development
- **Production Ready**: Handles concurrency well, stable
- **Minimal Configuration**: Works out of box with sensible defaults

### Alternatives Considered
- **Gunicorn + Uvicorn Workers**: More complex setup, better for very high traffic (not needed initially)
- **Hypercorn**: Alternative ASGI server, less popular than Uvicorn
- **Daphne**: Django-focused, not optimized for FastAPI

### Implementation Notes
- Development: `uvicorn app.main:app --reload`
- Production: `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`
- Workers: Number of CPU cores for production
- Logging: Configure via environment variables

---

## API Design Patterns

### Decision
**RESTful API** with standard HTTP methods

### Rationale
- **Industry Standard**: Well-understood patterns
- **FastAPI Strengths**: Excellent REST support with automatic OpenAPI docs
- **Simple for Blog**: CRUD operations map naturally to REST
- **Frontend Compatible**: Easy to consume from vanilla JavaScript

### Endpoint Structure
```
Authentication:
POST   /api/auth/register    - User registration
POST   /api/auth/login       - User login
POST   /api/auth/logout      - User logout
GET    /api/auth/me          - Current user info

Posts:
GET    /api/posts            - List posts (paginated)
POST   /api/posts            - Create post
GET    /api/posts/{id}       - Get single post
PUT    /api/posts/{id}       - Update post
DELETE /api/posts/{id}       - Delete post

Comments:
GET    /api/posts/{post_id}/comments     - List comments for post
POST   /api/posts/{post_id}/comments     - Create comment
PUT    /api/comments/{id}                - Update comment
DELETE /api/comments/{id}                - Delete comment

Users:
GET    /api/users/{id}       - Get user profile
```

### Response Format
- Success: JSON with data
- Error: JSON with `{"detail": "error message"}`
- Pagination: `{"items": [...], "total": N, "page": N, "size": N}`

### Alternatives Considered
- **GraphQL**: Overkill for simple blog, adds complexity, requires additional libraries
- **RPC Style**: Less standard, harder to document and consume

---

## Security Considerations

### Password Security
- **bcrypt hashing**: Industry standard, adaptive cost factor
- **Salt per password**: Automatic with bcrypt
- **Cost factor 12**: Balance of security and performance (adjustable)

### JWT Security
- **HTTP-only cookies**: XSS protection
- **Secure flag**: HTTPS-only transmission (production)
- **SameSite=lax**: CSRF protection
- **Short expiration**: 24 hours (requires re-login or refresh)
- **Secret rotation**: Environment variable, rotatable without code change

### Input Validation
- **Pydantic models**: Automatic validation at API boundary
- **Database constraints**: Foreign keys, unique constraints, not null
- **SQL injection**: Protected by ORM parameterized queries

### CORS Configuration
- **Development**: Allow localhost origins
- **Production**: Whitelist specific domains

### Rate Limiting
- **Future Enhancement**: Not implemented in v1, can add later with middleware

---

## Performance Optimizations

### Database
- **Indexes**: On foreign keys, username, email (unique), post author_id, comment post_id
- **Pagination**: Limit/offset for post listing (max 50 per page)
- **Eager Loading**: Use select_related/prefetch_related to avoid N+1 queries
- **WAL Mode**: SQLite Write-Ahead Logging for better concurrency

### Frontend
- **CSS**: Single minified file (~5-10KB)
- **JavaScript**: Minimal, only for progressive enhancement (~5-10KB)
- **Images**: No image uploads in v1, so bundle size minimal
- **Caching**: Browser caching headers for static assets

### API
- **Async/Await**: FastAPI + Tortoise ORM = non-blocking I/O
- **Connection Pooling**: Managed by Tortoise ORM
- **Response Compression**: Gzip middleware for API responses

---

## Development Workflow

### Project Structure
```
blog_app/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration management
│   ├── models/              # Tortoise ORM models
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── schemas/             # Pydantic schemas (request/response)
│   │   ├── user.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── routes/              # API endpoints
│   │   ├── auth.py
│   │   ├── posts.py
│   │   ├── comments.py
│   │   └── users.py
│   ├── services/            # Business logic
│   │   ├── auth.py
│   │   ├── post.py
│   │   └── comment.py
│   ├── dependencies/        # FastAPI dependencies
│   │   └── auth.py
│   └── templates/           # Jinja2 templates
│       ├── base.html
│       ├── index.html
│       ├── post.html
│       └── ...
├── static/                  # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── tests/                   # Test files
│   ├── test_auth.py
│   ├── test_posts.py
│   └── test_comments.py
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies (generated by uv)
├── .env.example             # Environment template
└── README.md
```

### Environment Configuration
```env
DATABASE_URL=sqlite://./blog.db
JWT_SECRET=<random-secret-key>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
BCRYPT_ROUNDS=12
ENVIRONMENT=development
```

---

## Deployment Considerations

### Development
- SQLite file in project root
- Uvicorn with `--reload`
- Debug mode enabled
- CORS open for localhost

### Production
- SQLite with WAL mode enabled
- Uvicorn with multiple workers
- HTTPS enforced (secure cookies)
- Environment variables for secrets
- CORS restricted to app domain
- Proper error logging

### Infrastructure
- Single VPS/container sufficient for initial launch
- 1GB RAM, 1 CPU core minimum
- Systemd service or Docker container
- Nginx reverse proxy (optional but recommended)
- Daily database backups (simple file copy)

---

## Open Questions RESOLVED

All technical decisions have been made based on user requirements:
- ✅ Backend framework: FastAPI
- ✅ Database: SQLite
- ✅ ORM: Tortoise ORM
- ✅ Migrations: Alembic
- ✅ Authentication: JWT (PyJWT) + bcrypt
- ✅ Frontend: Jinja2 + vanilla HTML/CSS/JS
- ✅ Testing: pytest
- ✅ Package management: uv
- ✅ Web server: Uvicorn

No NEEDS CLARIFICATION items remain.

---

## Next Steps

1. Generate data model based on specification entities
2. Define API contracts (OpenAPI schema)
3. Create quickstart guide for development setup
4. Proceed to implementation phase

