import json

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def build_valid_conversations_payload() -> bytes:
    payload = [
        {
            "id": "conversation-1",
            "mapping": {
                "node-user": {
                    "message": {
                        "author": {"role": "user"},
                        "content": {"parts": ["hello world"]},
                        "metadata": {},
                    }
                },
                "node-assistant": {
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {"parts": ["hello there"]},
                        "metadata": {"model_slug": "gpt-4o-mini"},
                    }
                },
            },
        }
    ]
    return json.dumps(payload).encode("utf-8")


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_import_valid_conversations_file():
    response = client.post(
        "/api/v1/import/conversations",
        files={"file": ("conversations.json", build_valid_conversations_payload(), "application/json")},
    )

    assert response.status_code == 200
    body = response.json()
    assert "global_stats" in body
    assert "conversation_stats" in body
    assert "model_stats" in body
    assert "meta" in body
    assert body["meta"]["conversations_received"] == 1


def test_import_rejects_wrong_filename():
    response = client.post(
        "/api/v1/import/conversations",
        files={"file": ("wrong_name.json", b"[]", "application/json")},
    )

    assert response.status_code == 400
    assert "conversations.json" in response.json()["detail"]


def test_import_rejects_invalid_json():
    response = client.post(
        "/api/v1/import/conversations",
        files={"file": ("conversations.json", b"{invalid", "application/json")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON file."


def test_import_rejects_invalid_conversation_shape():
    invalid_payload = json.dumps([{"id": "abc"}]).encode("utf-8")
    response = client.post(
        "/api/v1/import/conversations",
        files={"file": ("conversations.json", invalid_payload, "application/json")},
    )

    assert response.status_code == 422
    assert "Invalid conversation format" in response.json()["detail"]


def test_import_includes_cors_header_for_local_frontend():
    response = client.post(
        "/api/v1/import/conversations",
        files={"file": ("conversations.json", build_valid_conversations_payload(), "application/json")},
        headers={"Origin": "http://localhost:3000"},
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
