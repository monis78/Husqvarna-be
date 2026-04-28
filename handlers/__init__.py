import os
from typing import Optional
from authlib.integrations.httpx_client import AsyncOAuth2Client
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from jose import JWTError, jwt

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")  # In production, use environment variable
ALGORITHM = "HS256"

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_google_user_info(token: str):
    async with AsyncOAuth2Client(
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token=token
    ) as client:
        resp = await client.get('https://www.googleapis.com/oauth2/v2/userinfo')
        return resp.json()


def get_or_create_user(db: Session, google_id: Optional[str], email: str, name: str):
    user = None

    if google_id:
        user = db.query(User).filter(User.google_id == google_id).first()

    if not user:
        user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(google_id=google_id, email=email, name=name)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        changed = False
        if google_id and user.google_id != google_id:
            user.google_id = google_id
            changed = True
        if user.email != email:
            user.email = email
            changed = True
        if user.name != name:
            user.name = name
            changed = True

        if changed:
            db.commit()
            db.refresh(user)

    return user
