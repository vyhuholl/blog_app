"""
Integration tests for authentication API endpoints.

Tests user registration, login, logout, and current user endpoints.
"""


from app.services.auth import create_access_token


class TestAuthRegistration:
    """Test user registration endpoint."""

    def test_register_success(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/auth/register",
            json={"username": "newuser", "email": "new@example.com", "password": "password123"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "password" not in data
        assert "password_hash" not in data

        # Check cookie was set
        assert "access_token" in response.cookies

    def test_register_duplicate_username(self, client, test_user):
        """Test registration with duplicate username returns 409."""
        response = client.post(
            "/api/auth/register",
            json={
                "username": test_user.username,
                "email": "different@example.com",
                "password": "password123",
            },
        )

        assert response.status_code == 409
        assert "Username already exists" in response.json()["detail"]

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email returns 409."""
        response = client.post(
            "/api/auth/register",
            json={"username": "differentuser", "email": test_user.email, "password": "password123"},
        )

        assert response.status_code == 409
        assert "Email already exists" in response.json()["detail"]

    def test_register_invalid_data(self, client):
        """Test registration with invalid data returns 422."""
        response = client.post(
            "/api/auth/register", json={"username": "ab", "email": "invalid", "password": "short"}
        )

        assert response.status_code == 422


class TestAuthLogin:
    """Test user login endpoint."""

    def test_login_success(self, client, test_user):
        """Test successful user login."""
        response = client.post(
            "/api/auth/login", json={"username": "testuser", "password": "testpass123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email

        # Check cookie was set
        assert "access_token" in response.cookies

    def test_login_invalid_username(self, client):
        """Test login with invalid username returns 401."""
        response = client.post(
            "/api/auth/login", json={"username": "nonexistent", "password": "password"}
        )

        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]

    def test_login_invalid_password(self, client, test_user):
        """Test login with invalid password returns 401."""
        response = client.post(
            "/api/auth/login", json={"username": test_user.username, "password": "wrongpassword"}
        )

        assert response.status_code == 401
        assert "Invalid username or password" in response.json()["detail"]


class TestAuthLogout:
    """Test user logout endpoint."""

    def test_logout_success(self, client, test_user):
        """Test successful logout."""
        # First login
        token = create_access_token(test_user.id)

        response = client.post("/api/auth/logout", cookies={"access_token": token})

        assert response.status_code == 200
        assert "Successfully logged out" in response.json()["message"]

        # Verify that the logout response sets an expired/empty cookie
        # The set-cookie header should be present with max-age=0
        set_cookie_header = response.headers.get("set-cookie")
        assert set_cookie_header is not None
        assert "access_token" in set_cookie_header
        assert "max-age=0" in set_cookie_header.lower() or "expires" in set_cookie_header.lower()


class TestAuthMe:
    """Test current user endpoint."""

    def test_get_me_success(self, client, test_user):
        """Test getting current user with valid token."""
        token = create_access_token(test_user.id)

        response = client.get("/api/auth/me", cookies={"access_token": token})

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email

    def test_get_me_without_token(self, client):
        """Test getting current user without token returns 401."""
        response = client.get("/api/auth/me")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_get_me_invalid_token(self, client):
        """Test getting current user with invalid token returns 401."""
        response = client.get("/api/auth/me", cookies={"access_token": "invalid-token"})

        assert response.status_code == 401

