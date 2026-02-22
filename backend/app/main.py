from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import import_data

app = FastAPI(title="ChatGPT Wrapped")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(import_data.router)
