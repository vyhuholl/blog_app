"""
Template routes for serving HTML pages.

This module defines routes that render Jinja2 templates for the frontend.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models.post import Post
from app.models.user import User

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    """Render the index page with post list."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Render the registration page."""
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Render the login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/posts/new", response_class=HTMLResponse)
async def create_post_page(request: Request):
    """Render the create post page."""
    return templates.TemplateResponse("post_form.html", {"request": request, "post": None})


@router.get("/posts/{post_id}", response_class=HTMLResponse)
async def post_detail_page(request: Request, post_id: int):
    """Render the post detail page."""
    post = await Post.filter(id=post_id).prefetch_related("author").first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse("post_detail.html", {"request": request, "post": post})


@router.get("/posts/{post_id}/edit", response_class=HTMLResponse)
async def edit_post_page(request: Request, post_id: int):
    """Render the edit post page."""
    post = await Post.filter(id=post_id).prefetch_related("author").first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return templates.TemplateResponse("post_form.html", {"request": request, "post": post})


@router.get("/users/{user_id}", response_class=HTMLResponse)
async def user_profile_page(request: Request, user_id: int):
    """Render the user profile page."""
    user = await User.filter(id=user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get post count
    post_count = await Post.filter(author_id=user_id).count()

    return templates.TemplateResponse(
        "user_profile.html",
        {"request": request, "user": user, "post_count": post_count}
    )

