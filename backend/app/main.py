from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.config import UP_DIR, OUT_DIR, TMP_DIR

app = FastAPI(title="NEXO API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

for folder in [UP_DIR, OUT_DIR, TMP_DIR]:
    folder.mkdir(parents=True, exist_ok=True)