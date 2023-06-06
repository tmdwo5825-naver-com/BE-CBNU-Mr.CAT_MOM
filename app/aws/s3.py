import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import uuid
from app.core.config import settings
from fastapi import UploadFile, File


def s3_connection():
    try:
        s3 = boto3.client(
            's3',
            region_name=settings.s3_location,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3


def upload_file(image_byte: bytes, content_type: str = None) -> str:
    s3 = s3_connection()
    try:
        obj_name = uuid.uuid1()
        s3.put_object(
            Bucket=settings.s3_bucket_name,
            Key=obj_name.hex,
            Body=image_byte,
            ACL='public-read',
            ContentType=f'image/{content_type}'
        )
        print("uploaded file!")

    except ClientError as e:
        print(f'Credential error => {e}')
    except Exception as e:
        print(f"Another error => {e}")
    except NoCredentialsError as e:
        print(e)

    return obj_name.hex




