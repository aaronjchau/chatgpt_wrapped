from fastapi import APIRouter, File, UploadFile

router = APIRouter(prefix="/api/v1", tags=["import"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/import/conversations")
async def import_conversations(
    file: UploadFile = File(...),
):
    return {"status": "todo", "filename": file.filename}
