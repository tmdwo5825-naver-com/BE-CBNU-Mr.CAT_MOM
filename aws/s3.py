import configparser
import os
from pathlib import Path

from fastapi import UploadFile, File
from io import BytesIO
import boto3
import logging
from botocore.exceptions import ClientError


path = Path(__file__)
ROOT_DIR = path.parent.absolute()
config_path = os.path.join(ROOT_DIR, "config.ini")

config = configparser.ConfigParser()
config.read(config_path)

aws_access_key_id=config.get('s3', 'aws_access_key_id')
aws_secret_access_key=config.get('s3', 'aws_secret_access_key')

s3 = boto3.client(
    's3',
    aws_access_key_id,
    aws_secret_access_key
)

response = s3.list_buckets()

for bucket in response['Buckets']:
    print(f' {bucket["Name"]}')

def upload_file(image: UploadFile, created_at: str):
    image = BytesIO()
    image.seek()
    s3.upload_fileobj(
        image,
        "s3-cbnu-cat-mom",
        created_at
    )


def create_presigned_url(bucket_name, object_name, expiration=86400):
    s3_client = boto3.client('s3')
    try:
        url = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    return url
