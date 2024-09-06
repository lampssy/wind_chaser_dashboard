import logging
from typing import Generator

from botocore.exceptions import ClientError
from mypy_boto3_kinesis.client import KinesisClient

logger = logging.getLogger(__name__)


class KinesisStream:
    """Encapsulates a Kinesis stream."""

    def __init__(self, kinesis_client: KinesisClient):
        """
        Initializes the KinesisStream instance.

        Args:
            kinesis_client (KinesisClient): A Boto3 Kinesis client.
        """
        self.kinesis_client = kinesis_client
        self.name = None
        self.details = None
        self.stream_exists_waiter = kinesis_client.get_waiter("stream_exists")

    def describe(self, name: str) -> dict:
        """
        Gets metadata about a stream.

        Args:
            name (str): The name of the stream.

        Returns:
            dict: The stream's metadata
        """
        try:
            response = self.kinesis_client.describe_stream(StreamName=name)
            self.name = name
            self.details = response["StreamDescription"]
            logger.info(f"Got stream {name}.")
        except ClientError:
            logger.exception(f"Couldn't get {name} stream.")
            raise
        else:
            return self.details

    def get_records(self, max_records: int) -> Generator[list, None, None]:
        """
        Gets records from the stream. This function is a generator that first gets
        a shard iterator for the stream, then uses the shard iterator to get records
        in batches from the stream. Each batch of records is yielded back to the
        caller until the specified maximum number of records has been retrieved.

        Args:
            max_records (int): The maximum number of records to retrieve.

        Yields:
            list: The current batch of retrieved records.
        """
        try:
            response = self.kinesis_client.get_shard_iterator(
                StreamName=self.name,
                ShardId=self.details["Shards"][0]["ShardId"],
                ShardIteratorType="LATEST",
            )
            shard_iter = response["ShardIterator"]
            record_count = 0

            while record_count < max_records:
                response = self.kinesis_client.get_records(ShardIterator=shard_iter, Limit=10)
                shard_iter = response["NextShardIterator"]
                records = response["Records"]
                logger.info(f"Got {len(records)} records.")
                record_count += len(records)
                yield records

        except ClientError:
            logger.exception(f"Couldn't get records from stream {self.name}.")
            raise
