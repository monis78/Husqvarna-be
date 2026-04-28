# FastAPI Backend Server with Google OAuth

This is a FastAPI server with Google OAuth authentication, user management, PostgreSQL database, and Redis caching.

## Quick Start with Docker Compose

The easiest way to run the entire stack (FastAPI, PostgreSQL, Redis):

```bash
docker-compose up --build
```

This will start:
- **FastAPI App**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

The server will automatically create database tables on startup.

## Local Development Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up Google OAuth:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing
   - Enable Google+ API
   - Create OAuth 2.0 credentials
   - Add your frontend origin, such as `http://localhost:3000`, as an authorized JavaScript origin
   - Copy Client ID and Client Secret to `.env` file

3. Set up PostgreSQL locally:
   ```
   # macOS with Homebrew
   brew install postgresql
   brew services start postgresql
   
   # Or use Docker
   docker run -d --name postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:15-alpine
   ```

4. Update `.env` with your database credentials

5. Run the server:
   ```
   python -m uvicorn main:app --reload
   ```

The server will start on http://127.0.0.1:8000

## Environment Variables

See `.env` file for configuration options:
- `DATABASE_USER` - PostgreSQL username
- `DATABASE_PASSWORD` - PostgreSQL password
- `DATABASE_HOST` - PostgreSQL host
- `DATABASE_PORT` - PostgreSQL port
- `DATABASE_NAME` - PostgreSQL database name
- `REDIS_URL` - Redis connection URL
- `GOOGLE_CLIENT_ID` - Google OAuth Client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth Client Secret

## Endpoints

- `GET /`: Root endpoint to check if server is running
- `POST /api/v1/login`: Accepts a login token and returns an application access token

## Database

Uses PostgreSQL for user persistence. Tables are created automatically on startup.

## Docker

### Single service (FastAPI only):
```bash
docker build -t fastapi-oauth .
docker run -p 8000:8000 -e DATABASE_HOST=host.docker.internal fastapi-oauth
```

### Full stack with Docker Compose:
```bash
docker-compose up --build
```

### Stop services:
```bash
docker-compose down
```

### Remove volumes:
```bash
docker-compose down -v
```

## API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## Technologies

- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Relational database
- **Redis**: In-memory data store (ready for caching/sessions)
- **SQLAlchemy**: ORM for database operations
- **Authlib**: OAuth implementation
- **Docker & Docker Compose**: Containerization and orchestration
