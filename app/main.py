"""
FastAPI application initialization and configuration.

This module sets up the FastAPI application, database connections,
middleware, and routes.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from tortoise.contrib.fastapi import register_tortoise

from app.config import settings
from app.routes import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Handles database initialization and cleanup.
    """
    # Startup
    print("🚀 Starting up blog application...")
    yield
    # Shutdown
    print("👋 Shutting down blog application...")


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


# Import and register additional routers (will be added in later phases)

