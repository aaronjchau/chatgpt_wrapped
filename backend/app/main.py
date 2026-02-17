from fastapi import FastAPI
from app.api.routes import upload

app = FastAPI(title="ChatGPT Wrapped")

app.include_router(upload.router)
