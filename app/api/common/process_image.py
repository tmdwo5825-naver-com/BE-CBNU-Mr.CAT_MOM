from fastapi import UploadFile, File, HTTPException, status

from app.aws.s3 import upload_file
from app.core.config import settings


async def process_image(image: UploadFile = File(...), obj_name: str = None):
    print("async start")
    # 파일 처리 부분

    file_type = image.filename.split('.')[1].lower()
    print(file_type)

    if file_type == "jpeg" or file_type == "jpg" or file_type == "png":
        image_byte = await image.read()
        # 파일 s3에 업로드
        obj_name = upload_file(image_byte, obj_name)

        image_url = f'https://{settings.s3_bucket_name}.s3.amazonaws.com/{obj_name}'
        return image_url

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="허용되지 않은 이미지 형식")
