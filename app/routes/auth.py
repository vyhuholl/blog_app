"""
Authentication API routes.

This module defines endpoints for user registration, login, logout, and
current user information.
"""

from fastapi import APIRouter, Response, status

from app.dependencies.auth import CurrentUser
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister, UserResponse
from app.services.auth import authenticate_user, create_access_token, register_user

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, response: Response):
    """
    Register a new user account.

    Creates a new user with the provided username, email, and password.
    Returns user information and sets JWT token in HTTP-only cookie.
    """
    user = await register_user(user_data.username, user_data.email, user_data.password)

    # Create JWT token and set cookie
    token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
        max_age=86400,  # 24 hours
    )

    return UserResponse.model_validate(user)


@router.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin, response: Response):
    """
    Log in to an existing user account.

    Authenticates with username and password.
    Returns user information and sets JWT token in HTTP-only cookie.
    """
    user = await authenticate_user(credentials.username, credentials.password)

    # Create JWT token and set cookie
    token = create_access_token(user.id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,  # Set to True in production with HTTPS
        max_age=86400,  # 24 hours
    )

    return UserResponse.model_validate(user)


@router.post("/logout")
async def logout(response: Response):
    """
    Log out from the current session.

    Clears the JWT token cookie.
    """
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=0,  # Expire immediately
    )
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = CurrentUser):
    """
    Get information about the current authenticated user.

    Requires authentication.
    """
    return UserResponse.model_validate(current_user)

