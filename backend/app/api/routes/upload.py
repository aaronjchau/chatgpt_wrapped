from fastapi import APIRouter, HTTPException, UploadFile
from app.services import parser

router = APIRouter()


# route to import conversations.json and generate stats and plots
@router.post("/upload")
async def upload(file: UploadFile):