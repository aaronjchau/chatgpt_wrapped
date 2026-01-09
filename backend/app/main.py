from fastapi import FastAPI, APIRouter
from app.api.routes import upload

app = FastAPI(title="ChatGPT Wrapped")

app.include_router(upload.router)
