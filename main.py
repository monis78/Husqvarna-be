from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from models import Base
from routes import auth_router, llm_router
from middleware import AuthMiddleware
from config import API_V1_PREFIX, CORS_ALLOWED_ORIGINS

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add authentication middleware
app.add_middleware(AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=API_V1_PREFIX)
app.include_router(llm_router, prefix=API_V1_PREFIX)


@app.get("/")
def read_root():
    return {"message": "FastAPI server is running"}
