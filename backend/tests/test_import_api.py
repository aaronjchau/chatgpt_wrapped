import json

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def _valid_conversations_payload():
    return [
        {
            "id": "convo-1",
            "mapping": {
                "node-user": {
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["hello there"]},
                        "metadata": {},
                    }
                },
                "node-assistant": {
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {"parts": ["hi"]},
                        "metadata": {"model_slug": "gpt-4o"},
                    }
                },
            },
        }
    ]


def test_import_conversations_happy_path():
    payload = _valid_conversations_payload()
    files = {
        "file": (
            "conversations.json",
            json.dumps(payload),
            "application/json",
        )
    }

    response = client.post("/api/v1/import/conversations", files=files)

    assert response.status_code == 200
    body = response.json()
    assert "global_stats" in body
    assert "conversation_stats" in body
    assert "model_stats" in body
    assert "meta" in body
