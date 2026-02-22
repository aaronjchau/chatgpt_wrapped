import json

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services import parser, stats

router = APIRouter(prefix="/api/v1", tags=["import"])
MAX_IMPORT_BYTES = 250 * 1024 * 1024


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/import/conversations")
async def import_conversations(
    file: UploadFile = File(...),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided.")
    if file.filename != "conversations.json":
        raise HTTPException(
            status_code=400,
            detail="Expected a file named 'conversations.json'.",
        )

    raw_bytes = await file.read()
    if len(raw_bytes) > MAX_IMPORT_BYTES:
        raise HTTPException(status_code=413, detail="File is too large.")

    try:
        data = json.loads(raw_bytes)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON file.") from exc

    if not isinstance(data, list):
        raise HTTPException(
            status_code=422,
            detail="Expected top-level JSON array of conversations.",
        )

    try:
        all_messages = parser.parse(data)
        global_stats, conversation_stats, model_stats, time_stats = stats.compute_stats(all_messages)
    except (KeyError, TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=f"Invalid conversation format: {exc}") from exc

    return {
        "global_stats": global_stats,
        "conversation_stats": conversation_stats,
        "model_stats": model_stats,
        "time_stats": time_stats,
        "meta": {
            "conversations_received": len(data),
            "messages_parsed": len(all_messages),
        },
    }
