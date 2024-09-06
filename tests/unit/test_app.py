import json
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from httpx import Response

from app import app

client: TestClient = TestClient(app)


def test_read_root():
    response: Response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Windsurfing Monitoring System Dashboard! PS: I love Gosia <3"}


@patch("kinesis_stream.KinesisStream.get_records")
@patch("kinesis_stream.KinesisStream.describe")
def test_get_user_performance(mock_describe: MagicMock, mock_get_records: MagicMock):
    mock_describe.return_value = {"StreamDescription": {"Shards": [{"ShardId": "shardId-000000000000"}]}}
    mock_get_records.return_value = iter(
        [[{"Data": json.dumps({"user_id": 1, "performance": "data"}).encode("utf-8")}]]
    )

    response: Response = client.get("/performance?user_id=1")
    assert response.status_code == 200
    assert response.json() == {"user_id": 1, "performance": {"user_id": 1, "performance": "data"}}


@patch("kinesis_stream.KinesisStream.get_records")
@patch("kinesis_stream.KinesisStream.describe")
def test_get_weather_conditions(mock_describe: MagicMock, mock_get_records: MagicMock):
    mock_describe.return_value = {"StreamDescription": {"Shards": [{"ShardId": "shardId-000000000000"}]}}
    mock_get_records.return_value = iter([[{"Data": json.dumps({"weather": "sunny"}).encode("utf-8")}]])

    response: Response = client.get("/weather")
    assert response.status_code == 200
    assert response.json() == {"weather": {"weather": "sunny"}}
