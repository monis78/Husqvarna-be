from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os
from jose import jwt, JWTError
from config import API_V1_PREFIX

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

# Paths that don't require authentication
SKIP_AUTH_PATHS = [
    f"{API_V1_PREFIX}/login",
    f"{API_V1_PREFIX}/llm/query",
    f"{API_V1_PREFIX}/llm/query/stream",
    f"{API_V1_PREFIX}/llm/health",
    "/docs",
    "/openapi.json",
    "/redoc",
    "/"
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the current path requires authentication
        if request.url.path in SKIP_AUTH_PATHS:
            return await call_next(request)

        # Check for authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing authorization header")

        # Validate bearer token
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")
            
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)
