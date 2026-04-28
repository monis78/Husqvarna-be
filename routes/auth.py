import os
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session
from pydantic import BaseModel, validator
from database import get_db
from handlers import get_or_create_user, create_access_token
from jose import jwt, JWTError

router = APIRouter(tags=["auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


class LoginPayload(BaseModel):
    token: str

    @validator("token")
    def validate_token(cls, v):
        if not v or len(v) < 1:
            raise ValueError("Token is required")
        return v


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    picture: Optional[str] = None


class LoginResponse(BaseModel):
    token: str
    user: UserResponse


def verify_token_payload(token: str):
    """Verify and decode JWT token from payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


def verify_google_token(token: str):
    """Verify the Google ID token sent by the frontend login button."""
    if not GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google client ID is not configured")

    try:
        return id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginPayload, db: Session = Depends(get_db)):
    """Handle login with token validation"""
    try:
        if not payload.token:
            raise HTTPException(status_code=400, detail="Token is missing from payload")

        token_payload = verify_google_token(payload.token)

        if "sub" not in token_payload:
            raise HTTPException(
                status_code=401,
                detail="Invalid Google token: missing subject claim",
            )

        email = token_payload.get("email")
        if not email:
            raise HTTPException(
                status_code=401,
                detail="Invalid Google token: missing email claim",
            )

        user = get_or_create_user(
            db=db,
            google_id=token_payload["sub"],
            email=email,
            name=token_payload.get("name") or email.split("@")[0],
        )

        access_token = create_access_token(data={"sub": user.email})

        try:
            verify_token_payload(access_token)
        except HTTPException:
            raise HTTPException(status_code=500, detail="Failed to create valid token")

        return LoginResponse(
            token=access_token,
            user=UserResponse(
                id=str(user.id),
                email=user.email,
                name=user.name,
                picture=token_payload.get("picture"),
            ),
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
