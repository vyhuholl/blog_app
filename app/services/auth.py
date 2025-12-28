"""
Authentication service layer.

This module provides functions for password hashing, JWT token management,
user registration, and login logic.
"""

from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import HTTPException, status

from app.config import settings
from app.models.user import User


async def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password string
    """
    salt = bcrypt.gensalt(rounds=settings.bcrypt_rounds)
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def create_access_token(user_id: int) -> str:
    """
    Create a JWT access token for a user.

    Args:
        user_id: ID of the user

    Returns:
        Encoded JWT token string
    """
    expires_delta = timedelta(minutes=settings.jwt_expire_minutes)
    expire = datetime.utcnow() + expires_delta

    payload = {"user_id": user_id, "exp": expire}

    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        ) from e
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from e


async def register_user(username: str, email: str, password: str) -> User:
    """
    Register a new user.

    Args:
        username: Desired username
        email: User's email address
        password: Plain text password

    Returns:
        Created User object

    Raises:
        HTTPException: If username or email already exists
    """
    # Check if username already exists
    existing_username = await User.filter(username=username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username already exists"
        )

    # Check if email already exists
    existing_email = await User.filter(email=email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already exists"
        )

    # Hash password and create user
    password_hash = await hash_password(password)
    user = await User.create(username=username, email=email, password_hash=password_hash)

    return user


async def authenticate_user(username: str, password: str) -> User:
    """
    Authenticate a user with username and password.

    Args:
        username: Username to authenticate
        password: Plain text password

    Returns:
        Authenticated User object

    Raises:
        HTTPException: If credentials are invalid
    """
    user = await User.filter(username=username).first()

    if not user or not await verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password"
        )

    return user

