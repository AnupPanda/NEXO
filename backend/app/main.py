from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import UP_DIR, OUT_DIR, TMP_DIR
import os

# 1. CREATE FOLDERS FIRST
for folder in [UP_DIR, OUT_DIR, TMP_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# 2. NOW INITIALIZE APP AND ROUTES
from app.api.routes import router # Move this import here

app = FastAPI(title="NEXO API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)