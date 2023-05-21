import configparser
import os
from pathlib import Path

from fastapi import UploadFile, File
from io import BytesIO
import boto3
import logging
from botocore.exceptions import ClientError

import uuid


path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

AWS_ACCESS_KEY_ID = config.get('s3', 'aws_access_key_id')
AWS_SECRET_ACCESS_KEY = config.get('s3', 'aws_secret_access_key')

s3 = boto3.client(
    's3',
    region_name = 'ap-northeast-2',
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY
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
