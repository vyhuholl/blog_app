"""
FastAPI application initialization and configuration.

This module sets up the FastAPI application, database connections,
middleware, and routes.
"""

import logging
from contextlib import asynccontextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from tortoise.contrib.fastapi import register_tortoise

from app.config import settings
from app.routes import auth, comments, pages, posts, users

# ============================================
# LOGGING CONFIGURATION
# ============================================

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.environment == "production" else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(
            "logs/app.log", maxBytes=10485760, backupCount=5  # 10MB per file
        ),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Handles database initialization and cleanup.
    """
    # Startup
    logger.info("🚀 Starting up blog application...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database: {settings.database_url}")
    yield
    # Shutdown
    logger.info("👋 Shutting down blog application...")


# Initialize FastAPI application
app = FastAPI(
    title="Blog Application Platform",
    description="A modern blog platform with user authentication, posts, and comments",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"]
    if settings.environment == "development"
    else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Gzip compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add security headers to all responses.

    Args:
        request: FastAPI request object
        call_next: Next middleware in chain

    Returns:
        Response with security headers
    """
    response = await call_next(request)

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Add HSTS header in production
    if settings.environment == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Register Tortoise ORM
register_tortoise(
    app,
    db_url=settings.database_url,
    modules={"models": ["app.models.user", "app.models.post", "app.models.comment"]},
    generate_schemas=False,  # Use Alembic for migrations
    add_exception_handlers=True,
)


# ============================================
# ERROR HANDLERS
# ============================================


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions with custom error pages for HTML requests.

    Args:
        request: FastAPI request object
        exc: HTTP exception

    Returns:
        HTML error page or JSON response depending on request type
    """
    # Check if request is for HTML or API
    accept = request.headers.get("accept", "")

    if "text/html" in accept:
        # Return HTML error page
        if exc.status_code == 404:
            return templates.TemplateResponse(
                "404.html", {"request": request}, status_code=404
            )
        elif exc.status_code >= 500:
            return templates.TemplateResponse(
                "500.html", {"request": request}, status_code=exc.status_code
            )
        else:
            # For other HTTP errors, return JSON
            return JSONResponse(
                status_code=exc.status_code, content={"detail": str(exc.detail)}
            )
    else:
        # Return JSON for API requests
        return JSONResponse(
            status_code=exc.status_code, content={"detail": str(exc.detail)}
        )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with detailed error messages.

    Args:
        request: FastAPI request object
        exc: Validation exception

    Returns:
        JSON response with validation errors
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle uncaught exceptions with generic 500 error.

    Args:
        request: FastAPI request object
        exc: Exception

    Returns:
        HTML error page or JSON response depending on request type
    """
    import logging

    logger = logging.getLogger(__name__)
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    # Check if request is for HTML or API
    accept = request.headers.get("accept", "")

    if "text/html" in accept:
        return templates.TemplateResponse(
            "500.html", {"request": request}, status_code=500
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )


# ============================================
# ROUTES
# ============================================


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "status": "healthy",
        "message": "Blog Application Platform API",
        "version": "0.1.0",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Register authentication routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Register post routes
app.include_router(posts.router)

# Register comment routes
app.include_router(comments.router)

# Register user routes
app.include_router(users.router)

# Register page routes
app.include_router(pages.router, tags=["Pages"])

