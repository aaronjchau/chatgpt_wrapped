from fastapi import FastAPI
from app.api.routes import import_data

app = FastAPI(title="ChatGPT Wrapped")

app.include_router(import_data.router)
