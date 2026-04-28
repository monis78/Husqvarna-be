# Project Structure Documentation

## Directory Layout

```
backend/
├── models/
│   └── __init__.py       # SQLAlchemy models (User model)
├── handlers/
│   └── __init__.py       # Authentication handlers and utilities
├── routes/
│   ├── __init__.py       # Router exports
│   └── auth.py           # Login route (/api/v1/login)
├── main.py               # FastAPI application entry point
├── database.py           # SQLAlchemy and PostgreSQL configuration
├── docker-compose.yml    # Multi-service orchestration
├── Dockerfile            # Container configuration
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md             # Setup instructions
```

## Module Responsibilities

### `models/__init__.py`
Contains SQLAlchemy ORM models:
- **User**: Represents application users with Google OAuth integration
  - `id`: Primary key
  - `email`: Unique email address
  - `name`: User's name
  - `google_id`: Google OAuth ID (unique)

### `handlers/__init__.py`
Contains business logic and authentication functions:
- **create_access_token()**: Generates JWT access tokens
- **get_google_user_info()**: Fetches user info from Google OAuth
- **get_or_create_user()**: Database operation to create/retrieve users

### `routes/auth.py`
Contains API route handlers:
- **POST /api/v1/login**: Accepts a login token and returns an application access token

### `main.py`
FastAPI application initialization:
- Creates FastAPI app instance
- Initializes database tables
- Registers all routers
- Health check endpoint at GET /

### `database.py`
PostgreSQL configuration:
- Creates SQLAlchemy engine
- Sets up session management
- Provides dependency injection for database sessions

## Import Pattern

The project uses modular imports as follows:

```python
# In main.py
from models import Base, User
from handlers import create_access_token, get_google_user_info, get_or_create_user
from routes import auth_router
```

This keeps the main.py clean and organizes code by responsibility.

## Adding New Features

### Adding a New Route:
1. Create `routes/new_feature.py` with an APIRouter
2. Export it in `routes/__init__.py`
3. Include it in `main.py` with `app.include_router()`

### Adding a New Handler:
1. Add function to `handlers/__init__.py`
2. Import in `routes/` where needed

### Adding a New Model:
1. Add SQLAlchemy class to `models/__init__.py`
2. Perform migrations if needed

## Legacy Files (Can be Deleted)
- `auth.py` - Replaced by `handlers/__init__.py`
- `models.py` - Replaced by `models/__init__.py`
