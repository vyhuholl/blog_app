# API Contracts Documentation

**Feature**: Blog Application Platform  
**Constitution Version**: 1.0.0  
**Date**: 2025-12-28

---

## Overview

This document describes the REST API contracts for the blog application platform. The complete OpenAPI 3.1 specification is available in `openapi.yaml`.

---

## API Design Principles

### REST Standards
- Standard HTTP methods: GET, POST, PUT, DELETE
- Resource-oriented URLs
- JSON request/response bodies
- HTTP status codes for response states

### Authentication
- JWT token-based authentication
- Tokens stored in HTTP-only cookies
- Cookie name: `access_token`
- Token expiration: 24 hours

### Response Format
All successful responses return JSON. Errors follow consistent format:
```json
{
  "detail": "Error message description"
}
```

### Pagination
List endpoints support pagination with query parameters:
- `page`: Page number (1-indexed, default: 1)
- `page_size`: Items per page (1-50, default: 20)

Response includes:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

---

## Endpoint Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| **Authentication** |
| POST | `/api/auth/register` | No | Register new user account |
| POST | `/api/auth/login` | No | Login to existing account |
| POST | `/api/auth/logout` | Yes | Logout from session |
| GET | `/api/auth/me` | Yes | Get current user info |
| **Posts** |
| GET | `/api/posts` | No | List all posts (paginated) |
| POST | `/api/posts` | Yes | Create new post |
| GET | `/api/posts/{post_id}` | No | Get single post details |
| PUT | `/api/posts/{post_id}` | Yes | Update post (author only) |
| DELETE | `/api/posts/{post_id}` | Yes | Delete post (author only) |
| **Comments** |
| GET | `/api/posts/{post_id}/comments` | No | List comments for post |
| POST | `/api/posts/{post_id}/comments` | Yes | Add comment to post |
| PUT | `/api/comments/{comment_id}` | Yes | Update comment (author only) |
| DELETE | `/api/comments/{comment_id}` | Yes | Delete comment (author only) |
| **Users** |
| GET | `/api/users/{user_id}` | No | Get user public profile |

---

## Authentication Flow

### Registration
```
POST /api/auth/register
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepass123"
}

Response: 201 Created
Set-Cookie: access_token=eyJhbGc...; HttpOnly; Path=/; SameSite=Lax

{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepass123"
}

Response: 200 OK
Set-Cookie: access_token=eyJhbGc...; HttpOnly; Path=/; SameSite=Lax

{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

### Logout
```
POST /api/auth/logout
Cookie: access_token=eyJhbGc...

Response: 200 OK
Set-Cookie: access_token=; HttpOnly; Path=/; Max-Age=0

{
  "message": "Successfully logged out"
}
```

### Get Current User
```
GET /api/auth/me
Cookie: access_token=eyJhbGc...

Response: 200 OK

{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

---

## Posts API

### List Posts
```
GET /api/posts?page=1&page_size=20

Response: 200 OK

{
  "items": [
    {
      "id": 1,
      "title": "My First Blog Post",
      "author": {
        "id": 1,
        "username": "johndoe",
        "created_at": "2025-12-28T10:00:00Z"
      },
      "created_at": "2025-12-28T10:00:00Z"
    }
  ],
  "total": 100,
  "page": 1,
  "page_size": 20,
  "total_pages": 5
}
```

### Create Post
```
POST /api/posts
Cookie: access_token=eyJhbGc...
Content-Type: application/json

{
  "title": "My First Blog Post",
  "content": "This is the content of my blog post."
}

Response: 201 Created

{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my blog post.",
  "author": {
    "id": 1,
    "username": "johndoe",
    "created_at": "2025-12-28T10:00:00Z"
  },
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z"
}
```

### Get Post
```
GET /api/posts/1

Response: 200 OK

{
  "id": 1,
  "title": "My First Blog Post",
  "content": "This is the content of my blog post.",
  "author": {
    "id": 1,
    "username": "johndoe",
    "created_at": "2025-12-28T10:00:00Z"
  },
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:00:00Z"
}
```

### Update Post
```
PUT /api/posts/1
Cookie: access_token=eyJhbGc...
Content-Type: application/json

{
  "title": "Updated Post Title",
  "content": "Updated content."
}

Response: 200 OK

{
  "id": 1,
  "title": "Updated Post Title",
  "content": "Updated content.",
  "author": {
    "id": 1,
    "username": "johndoe",
    "created_at": "2025-12-28T10:00:00Z"
  },
  "created_at": "2025-12-28T10:00:00Z",
  "updated_at": "2025-12-28T10:30:00Z"
}
```

### Delete Post
```
DELETE /api/posts/1
Cookie: access_token=eyJhbGc...

Response: 204 No Content
```

---

## Comments API

### List Comments
```
GET /api/posts/1/comments

Response: 200 OK

[
  {
    "id": 1,
    "content": "Great post! Thanks for sharing.",
    "author": {
      "id": 2,
      "username": "janedoe",
      "created_at": "2025-12-28T09:00:00Z"
    },
    "post_id": 1,
    "created_at": "2025-12-28T11:00:00Z",
    "updated_at": "2025-12-28T11:00:00Z"
  }
]
```

### Create Comment
```
POST /api/posts/1/comments
Cookie: access_token=eyJhbGc...
Content-Type: application/json

{
  "content": "Great post! Thanks for sharing."
}

Response: 201 Created

{
  "id": 1,
  "content": "Great post! Thanks for sharing.",
  "author": {
    "id": 2,
    "username": "janedoe",
    "created_at": "2025-12-28T09:00:00Z"
  },
  "post_id": 1,
  "created_at": "2025-12-28T11:00:00Z",
  "updated_at": "2025-12-28T11:00:00Z"
}
```

### Update Comment
```
PUT /api/comments/1
Cookie: access_token=eyJhbGc...
Content-Type: application/json

{
  "content": "Updated comment text."
}

Response: 200 OK

{
  "id": 1,
  "content": "Updated comment text.",
  "author": {
    "id": 2,
    "username": "janedoe",
    "created_at": "2025-12-28T09:00:00Z"
  },
  "post_id": 1,
  "created_at": "2025-12-28T11:00:00Z",
  "updated_at": "2025-12-28T11:15:00Z"
}
```

### Delete Comment
```
DELETE /api/comments/1
Cookie: access_token=eyJhbGc...

Response: 204 No Content
```

---

## Users API

### Get User Profile
```
GET /api/users/1

Response: 200 OK

{
  "id": 1,
  "username": "johndoe",
  "created_at": "2025-12-28T10:00:00Z"
}
```

---

## HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | Successful GET, PUT requests |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation errors, malformed JSON |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized for action |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Unique constraint violation (e.g., duplicate username) |
| 500 | Internal Server Error | Unexpected server error |

---

## Error Response Examples

### Validation Error
```json
{
  "detail": "Password must be at least 8 characters"
}
```

### Authentication Error
```json
{
  "detail": "Not authenticated"
}
```

### Authorization Error
```json
{
  "detail": "You can only update your own posts"
}
```

### Not Found Error
```json
{
  "detail": "Post not found"
}
```

### Conflict Error
```json
{
  "detail": "Username already exists"
}
```

---

## Security Considerations

### Authentication Token
- Stored in HTTP-only cookie (prevents XSS attacks)
- SameSite=Lax (CSRF protection)
- Secure flag in production (HTTPS only)
- 24-hour expiration

### Input Validation
- All inputs validated via Pydantic schemas
- Field length limits enforced
- Pattern validation for username (alphanumeric + underscore)
- Email format validation

### Authorization
- Ownership checks before update/delete operations
- Only post/comment authors can modify their content
- Public endpoints accessible without authentication

### CORS
- Development: Localhost origins allowed
- Production: Whitelist specific domains

---

## Rate Limiting

Not implemented in v1. Future enhancement considerations:
- Authentication endpoints: 5 requests/minute
- Post creation: 10 requests/hour
- Comment creation: 30 requests/hour
- Read endpoints: 100 requests/minute

---

## Versioning Strategy

Current version: v1 (implicit in URLs)

Future versioning approach:
- Breaking changes: New API version (e.g., `/api/v2/posts`)
- Non-breaking changes: Same version, extend existing contracts
- Deprecation: 6-month notice before removal

---

## Testing the API

### Using curl

**Register**:
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","email":"john@example.com","password":"securepass123"}' \
  -c cookies.txt
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"johndoe","password":"securepass123"}' \
  -c cookies.txt
```

**Create Post**:
```bash
curl -X POST http://localhost:8000/api/posts \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"title":"My First Post","content":"This is my first blog post!"}'
```

**List Posts**:
```bash
curl http://localhost:8000/api/posts
```

### Using OpenAPI UI

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow testing all endpoints directly from the browser.

---

## Frontend Integration

### JavaScript Fetch Example

```javascript
// Register user
async function register(username, email, password) {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, email, password }),
    credentials: 'include', // Important: include cookies
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
}

// Create post
async function createPost(title, content) {
  const response = await fetch('/api/posts', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ title, content }),
    credentials: 'include',
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  return await response.json();
}

// List posts with pagination
async function listPosts(page = 1, pageSize = 20) {
  const response = await fetch(`/api/posts?page=${page}&page_size=${pageSize}`);
  
  if (!response.ok) {
    throw new Error('Failed to load posts');
  }
  
  return await response.json();
}
```

**Important**: Always include `credentials: 'include'` in fetch options to send cookies with requests.

---

## Next Steps

1. Implement API routes in FastAPI (`app/routes/`)
2. Create Pydantic schemas for validation (`app/schemas/`)
3. Implement business logic in service layer (`app/services/`)
4. Add authentication dependencies (`app/dependencies/auth.py`)
5. Test all endpoints with pytest
6. Integrate with frontend templates

