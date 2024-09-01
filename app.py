import json

import boto3
from fastapi import FastAPI
from mypy_boto3_kinesis.client import KinesisClient
from mypy_boto3_kinesis.type_defs import GetRecordsOutputTypeDef

app = FastAPI()

kinesis_client: KinesisClient = boto3.client("kinesis", region_name="us-west-2")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Windsurfing Monitoring System Dashboard! PS: I love Gosia <3"}


@app.get("/performance")
def get_user_performance(user_id: int) -> dict:
    """
    Retrieve and return user performance data from Kinesis stream.
    """
    response: GetRecordsOutputTypeDef = kinesis_client.get_records(
        StreamName="performance-stream", ShardIteratorType="LATEST"
    )
    records = response["Records"]
    performance_data = {}
    for record in records:
        data = json.loads(record["Data"])
        if data["user_id"] == user_id:
            performance_data = data
            break
    return {"user_id": user_id, "performance": performance_data}


@app.get("/weather")
def get_weather_conditions() -> dict:
    """
    Retrieve and return current weather conditions from Kinesis stream.
    """
    response: GetRecordsOutputTypeDef = kinesis_client.get_records(
        StreamName="weather-stream", ShardIteratorType="LATEST"
    )
    records = response["Records"]
    weather_data = {}
    if records:
        weather_data = json.loads(records[0]["Data"])
    return {"weather": weather_data}


@app.get("/sessions")
def get_track_sessions(user_id: int) -> dict:
    """
    Retrieve and return data for past sessions from Kinesis stream.
    """
    response: GetRecordsOutputTypeDef = kinesis_client.get_records(
        StreamName="sessions-stream", ShardIteratorType="LATEST"
    )
    records = response["Records"]
    sessions_data = []
    for record in records:
        data = json.loads(record["Data"])
        if data["user_id"] == user_id:
            sessions_data.append(data)
    return {"user_id": user_id, "sessions": sessions_data}
