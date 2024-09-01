import json
from typing import Any, Dict
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from httpx import Response

from app import app, kinesis_client

client: TestClient = TestClient(app)


def test_read_root() -> None:
    response: Response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Windsurfing Monitoring System Dashboard! PS: I love Gosia <3"}


@patch.object(kinesis_client, "get_records")
def test_get_user_performance(mock_get_records: MagicMock) -> None:
    mock_response: Dict[str, Any] = {
        "Records": [{"Data": json.dumps({"user_id": 1, "performance": "data"}).encode("utf-8")}]
    }
    mock_get_records.return_value = mock_response

    response: Response = client.get("/performance?user_id=1")
    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "performance": {"user_id": 1, "performance": "data"},
    }


@patch.object(kinesis_client, "get_records")
def test_get_weather_conditions(mock_get_records: MagicMock) -> None:
    mock_response: Dict[str, Any] = {"Records": [{"Data": json.dumps({"weather": "sunny"}).encode("utf-8")}]}
    mock_get_records.return_value = mock_response

    response: Response = client.get("/weather")
    assert response.status_code == 200
    assert response.json() == {"weather": {"weather": "sunny"}}
