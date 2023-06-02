from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.crud_cat import crud_cat
from app.aws.s3 import upload_file
from app.core.config import settings
from app.database.set_mysql import engine
from app.api.deps import check_location, get_db

import time

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/content-create/", description="file upload 및 mysql db,redis db에 content 추가.")
async def create_content(
        comment: str = Form(default=None, description="사진에 추가할 코멘트"),
        lat: float = Form(description="float형 위도"),
        lon: float = Form(description="경도"),
        image: UploadFile = File(description="클라이언트가 업로드할 이미지, 이미지 형식은 미정(아직은 jpeg만 처리한다.)"),
        db: Session = Depends(get_db)
):
    start = time.time()
    print(image.filename)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )

    # 파일 처리 부분
    file_type = image.filename.split('.')[1].lower()

    # 파일 s3에 업로드
    obj_name = await upload_file(image, file_type)
    print(file_type)
    image_url = f'https://{settings.s3_bucket_name}.s3.amazonaws.com/{obj_name}'

    # 객체 처리
    cat_tower = check_location(lat, lon)
    request = schemas.CatCreate(comment=comment, image_url=image_url, x=lon, y=lat, cat_tower=cat_tower)

    # db 저장
    crud_cat.create_24h_content(db, request)
    print("db done")

    # redis 저장
    crud_cat.create_3h_content(request)

    end = time.time()
    result = end - start
    print(result)

    # os.remove(path)
    # os.remove("image.png")

    return HTTPException(status_code=status.HTTP_201_CREATED)


# 3시간 이내 데이터 조회
@router.get("/3hours", description="3시간 이내의 데이터를 조회한다.")
def get_3h_contents():
    start = time.time()
    response = crud_cat.get_3h()
    end = time.time()
    print(end - start)
    return {"data": response}


# 24시간 데이터 조회
@router.get("/today", description="24시간 이내의 데이터를 조회한다.")
def get_content(db: Session = Depends(get_db)):
    start = time.time()
    response = crud_cat.get_24h(db)
    end = time.time()
    print(end - start)
    return {"data": response}


@router.get("/count", description="캣타워 데이터의 개수를 반환한다.")
def get_count_of_data():
    response = crud_cat.count_data()
    return response


# 테스트
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # 파일 이름 얻기
    filename = file.filename

    # 파일 내용 읽기 (as bytes)
    contents = await file.read()
    upload_file(filename,)