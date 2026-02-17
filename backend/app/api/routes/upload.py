from fastapi import APIRouter

from app.services import parser, stats

router = APIRouter(prefix="/api/v1", tags=["upload"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/upload/conversations")
def upload_conversations():
    data = parser.load_conversations()
    all_messages = parser.parse(data)
    global_stats, conversation_stats, model_stats = stats.compute_stats(all_messages)

    return {
        "global_stats": global_stats,
        "conversation_stats": conversation_stats,
        "model_stats": model_stats,
    }
