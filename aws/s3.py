from fastapi import UploadFile, File
from io import BytesIO
import boto3
import logging
from botocore.exceptions import ClientError
from ..core.config import settings

import uuid


s3 = boto3.client(
    's3',
    region_name='ap-northeast-2',
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key
)


def upload_file(image: UploadFile) -> str:
    image = BytesIO()
    image.seek()

    obj_name = uuid.uuid1()

    s3.upload_fileobj(
        image,
        "s3-cbnu-cat-mom",
        obj_name
    )
    return obj_name


def create_presigned_url(bucket_name, obj_name, expiration=1800):
    s3_client = boto3.client('s3')
    try:
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name,
                    'Key': obj_name},
            ExpiresIn=expiration
            )

    except ClientError as e:
        logging.error(e)
        return None

    return url
