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
                        "create_time": 1735776000,
                    }
                },
                "node-assistant": {
                    "message": {
                        "author": {"role": "assistant"},
                        "content": {"parts": ["hi"]},
                        "metadata": {"model_slug": "gpt-4o"},
                        "create_time": 1735776015,
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
    assert "time_stats" in body
    assert "meta" in body


def test_import_conversations_rejects_wrong_filename():
    payload = _valid_conversations_payload()
    files = {
        "file": (
            "wrong_name.json",
            json.dumps(payload),
            "application/json",
        )
    }

    response = client.post("/api/v1/import/conversations", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Expected a file named 'conversations.json'."


def test_import_conversations_rejects_invalid_json():
    files = {
        "file": (
            "conversations.json",
            '{"not valid json"',
            "application/json",
        )
    }

    response = client.post("/api/v1/import/conversations", files=files)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON file."


def test_import_conversations_rejects_invalid_shape():
    files = {
        "file": (
            "conversations.json",
            json.dumps({"not": "a list"}),
            "application/json",
        )
    }

    response = client.post("/api/v1/import/conversations", files=files)

    assert response.status_code == 422
    assert response.json()["detail"] == "Expected top-level JSON array of conversations."


def test_import_conversations_allows_localhost_origin():
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
    }

    response = client.options("/api/v1/import/conversations", headers=headers)

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


def test_import_conversations_returns_time_stats():
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
    time_stats = body["time_stats"]

    assert "msgs_sent_by_hour" in time_stats
    assert "msgs_sent_by_day" in time_stats
    assert "msgs_sent_by_month" in time_stats
    assert "msgs_sent_by_year" in time_stats
    assert "msgs_sent_rolling_12mo" in time_stats

    assert sum(time_stats["msgs_sent_by_hour"].values()) == 1
    assert sum(time_stats["msgs_sent_by_day"].values()) == 1
    assert sum(time_stats["msgs_sent_by_month"].values()) == 1
    assert sum(time_stats["msgs_sent_by_year"].values()) == 1

    rolling = time_stats["msgs_sent_rolling_12mo"]
    assert len(rolling) == 365
    assert sum(day["count"] for day in rolling) == 1
