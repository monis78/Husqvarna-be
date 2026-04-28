# Fullstack AI Backend

A FastAPI-based backend application for a fullstack AI project, providing authentication and LLM (Large Language Model) services. The application integrates with PostgreSQL for data persistence and Redis for caching.

## Features

- **Authentication**: User registration, login, and JWT-based authentication.
- **LLM Integration**: API endpoints for interacting with language models (e.g., OpenAI).
- **Database**: PostgreSQL for storing user data and application state.
- **Caching**: Redis for session management and performance optimization.
- **CORS Support**: Configured for frontend integration (default: localhost:3000).
- **Containerized**: Docker support for easy deployment.

## Tech Stack

- **Framework**: FastAPI (Python web framework for APIs).
- **Database**: PostgreSQL with SQLAlchemy ORM.
- **Cache**: Redis.
- **Authentication**: JWT with Authlib.
- **LLM**: LangChain with OpenAI integration.
- **Other**: Uvicorn (ASGI server), Pydantic for data validation.

## Future extension
- **Pg vector**: For Rag based and context engineering
- **RabbitMq**: For async request handling and scalling.
- **LLM**: Langgraph and MCP server for agentic ai.
- **Graph database**: Neo4j for graph rag.


## Prerequisites

- Python 3.11+
- Docker and Docker Compose (for containerized setup)
- PostgreSQL (if running locally without Docker)
- Redis (if running locally without Docker)

## Installation and Setup

### Local Development

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up PostgreSQL and Redis locally using docker-compose file.

4. Create a `.env` file as above, adjusting environment variables for local services.

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

   Access at `http://localhost:8000`.

## API Endpoints

- `GET /`: Health check endpoint.
- `POST /api/v1/auth/register`: User registration.
- `POST /api/v1/auth/login`: User login.
- `GET /api/v1/llm/...`: LLM-related endpoints (details in routes/llm.py).

For full API documentation, visit `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` when the app is running.

## Assumptions

- The frontend is a React application running on `http://localhost:3000` (configured in CORS_ALLOWED_ORIGINS).
- Environment variables are set for database, Redis,Open ai, Auth and API keys.
- PostgreSQL and Redis are available (via Docker Compose).
- The application is deployed in a containerized environment for production (see DEPLOYMENT.md).

## Decisions Made

- **FastAPI**: Chosen for its speed, async support, and automatic API documentation generation.
- **SQLAlchemy**: ORM for database interactions, providing flexibility and scalability.
- **JWT Authentication**: Stateless authentication suitable for APIs.
- **LangChain + OpenAI**: For LLM integration, enabling easy AI-powered features.
- **Docker**: Ensures consistent environments across development and production.
- **PostgreSQL**: For production readiness and Pg vector support.
- **Redis**: For caching and session management to improve performance.
- **CORS Middleware**: To allow frontend-backend communication during development.
