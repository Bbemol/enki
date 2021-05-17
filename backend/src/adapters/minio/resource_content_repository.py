from typing import Union

import os

from minio import Minio
from urllib3.exceptions import MaxRetryError


class ClientNotInitializedError(Exception):
    pass


class MinioResourceContentRepository:
    """

    """

    @classmethod
    def from_config(cls, config):
        return cls(minio_uri=config.MINIO_URI,
                   access_key=config.MINIO_ACCESS_KEY,
                   secret_key=config.MINIO_SECRET_KEY,
                   region=config.MINIO_REGION,
                   secure=config.MINIO_SECURE,
                   bucket_list=[
                       config.MINIO_MESSAGE_RESOURCES_BUCKET
                   ])

    def __init__(self, minio_uri: str, access_key: str, secret_key: str, region:str, secure:bool, bucket_list: Union[list, None] = None):
        self.bucket_list = bucket_list or []


        self.client = Minio(minio_uri,
                            access_key=access_key,
                            secret_key=secret_key,
                            region=region,
                            secure=secure)
        self.initialize()

    def initialize(self):
        for bucket in self.bucket_list:
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket)

    def _exists(self, bucket: str, object_path: str) -> bool:
        stats = self.client.stat_object(
            bucket_name=bucket,
            object_name=object_path,
        )
        if stats:
            return True
        else:
            return False

    def list_objects(self, bucket: str, path: str):
        if self.client:
            objects = self.client.list_objects(bucket=bucket, prefix=path)
            return objects
        else:
            raise ClientNotInitializedError

    def get_presigned_get_url(self, bucket: str, object_path: str) -> str:
        url = self.client.presigned_get_object(
            bucket_name=bucket,
            object_name=object_path,
        )
        return url

    def get_presigned_put_url(self, bucket: str, object_path: str) -> str:
        url = self.client.presigned_put_object(
            bucket_name=bucket,
            object_name=object_path,
        )
        return url

    def get_presigned_delete_url(self, bucket: str, object_path: str) -> str:
        url = self.client.get_presigned_url(
            "DELETE",
            bucket_name=bucket,
            object_name=object_path,
        )
        return url
