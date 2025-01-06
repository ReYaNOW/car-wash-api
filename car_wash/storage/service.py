import functools
import inspect
import logging
import uuid
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncGenerator

from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile
from types_aiobotocore_s3.client import S3Client

from car_wash.config import config
from car_wash.storage.schemas import S3Folders

info_logger = logging.getLogger('uvicorn.debug')
error_logger = logging.getLogger('uvicorn.error')

UPLOAD_CHUNK_SIZE = 5 * 1024 * 1024  # 5 Mb
EXPIRATION = 3600  # 1 Hour


class S3Service:
    def __init__(self):
        self.config = {
            'aws_access_key_id': config.s3_access_key,
            'aws_secret_access_key': config.s3_secret_access_key,
            'endpoint_url': config.s3_server_url.unicode_string().replace(
                config.s3_server_url.host, 'minio'
            ),
            'use_ssl': config.use_ssl,
        }
        self.bucket_name = config.default_bucket
        self.session = get_session()

    @asynccontextmanager
    async def create_client(self) -> AsyncContextManager[S3Client]:
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    def display_exception(
        self, e: ClientError, args: Any, kwargs: Any
    ) -> None:
        error_code = e.response['Error']['Code']
        filename = kwargs.get('filename', args[0] if args else None)

        match error_code:
            case 'NoSuchKey' if isinstance(filename, str):
                raise HTTPException(
                    status_code=404,
                    detail=f'File not found: {filename}',
                ) from None

            case 'BucketAlreadyOwnedByYou':
                pass

            case _:
                raise HTTPException(status_code=500, detail=str(e)) from e

    @staticmethod
    def error_handler(func: Any) -> Any:
        @functools.wraps(func)
        async def wrapper(
            self: 'S3Service', *args: Any, **kwargs: Any
        ) -> AsyncGenerator | Any:
            async def generator_wrapper(
                self: 'S3Service', *args: Any, **kwargs: Any
            ) -> AsyncGenerator:
                try:
                    async for value in func(self, *args, **kwargs):
                        yield value
                except ClientError as e:
                    self.display_exception(e, args, kwargs)

            try:
                if inspect.isasyncgenfunction(func):
                    return generator_wrapper(self, *args, **kwargs)
                result = await func(self, *args, **kwargs)
            except ClientError as e:
                self.display_exception(e, args, kwargs)
            else:
                return result

        return wrapper

    @error_handler
    async def upload_file(
        self,
        directory: S3Folders,
        file: UploadFile,
        filepath: str | None = None,
    ) -> str:
        if not filepath:
            unique_fn = uuid.uuid4()
            filepath = f'{directory.value}/{unique_fn}'

        async with self.create_client() as client:
            client: S3Client
            try:
                resp = await client.create_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=filepath,
                    ContentType=file.content_type,
                )
                upload_id = resp['UploadId']
                parts = []
                part_number = 1
                while True:
                    chunk = await file.read(UPLOAD_CHUNK_SIZE)
                    if not chunk:
                        break

                    part = await client.upload_part(
                        Body=chunk,
                        Bucket=self.bucket_name,
                        Key=filepath,
                        UploadId=upload_id,
                        PartNumber=part_number,
                    )
                    parts.append(
                        {'ETag': part['ETag'], 'PartNumber': part_number}
                    )
                    part_number += 1
                await client.complete_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=filepath,
                    UploadId=upload_id,
                    MultipartUpload={'Parts': parts},
                )

            except ClientError:
                await client.abort_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=filepath,
                    UploadId=upload_id,
                )
                raise
        return filepath

    async def generate_link(self, filename: str) -> str:
        async with self.create_client() as client:
            client: S3Client
            url = await client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': filename},
                ExpiresIn=EXPIRATION,
            )
            return url.replace('minio', config.s3_server_url.host)

    @error_handler
    async def remove_file(self, filename: str) -> None:
        async with self.create_client() as client:
            client: S3Client
            await client.delete_object(Bucket=self.bucket_name, Key=filename)

    @error_handler
    async def find_files(
        self, pattern: str
    ) -> dict[str, list[dict[str, str]]]:
        async with self.create_client() as client:
            client: S3Client

            paginator = client.get_paginator('list_objects_v2')
            result = []
            async for page in paginator.paginate(Bucket=self.bucket_name):
                for obj in page.get('Contents', []):
                    if pattern in obj['Key']:
                        filename = obj['Key']
                        head_response = await client.head_object(
                            Bucket=self.bucket_name, Key=filename
                        )
                        content_type = head_response.get(
                            'ContentType', 'application/octet-stream'
                        )
                        result.append(
                            {
                                'file_name': filename,
                                'content_type': content_type,
                            }
                        )
        return {'files': result}

    @error_handler
    async def create_default_bucket(self) -> None:
        async with self.create_client() as client:
            client: S3Client
            await client.create_bucket(Bucket=self.bucket_name)
