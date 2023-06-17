from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.crud_mysql import crud_mysql
from app.crud.crud_redis import crud_redis
from app.database.set_mysql import engine, get_db
from app.api.common.get_cat_tower import check_location
from app.api.common.process_image import process_image
from app.api.common.process_time import process_time

import uuid

import time

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/content-create/", description="file upload 및 mysql db,redis db에 content 추가.")
async def create_content(
        comment: str = Form(default=None, description="사진에 추가할 코멘트"),
        lat: float = Form(description="float형 위도"),
        lon: float = Form(description="경도"),
        image: UploadFile = File(description="클라이언트가 업로드할 이미지"),
        month: int = Form(description="업로드 월"),
        day: int = Form(description="업로드 일"),
        hour: int = Form(description="업로드 시간"),
        min: int = Form(description="업로드 분"),
        db: Session = Depends(get_db)
):
    start = time.time()
    print(image.filename)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )

    # 이미지 처리
    obj_name = uuid.uuid1().hex
    print(obj_name + "1")
    image_url = await process_image(image, obj_name)

    # 객체 처리
    print("doing another task")
    cat_tower = await check_location(lat, lon)

    # db 저장
    upload_time = process_time.get_static_time(day, hour, min)
    request_mysql = schemas.CatCreateMysql(comment=comment, image_url=image_url, x=lon, y=lat, upload_time=upload_time)
    crud_mysql.create_24h_content(db, request_mysql)
    print("db done")

    # redis 저장
    request_redis = schemas.CatCreateRedis(comment=comment, image_url=image_url, x=lon, y=lat, cat_tower=cat_tower, hour=hour, min=min)
    crud_redis.create_3h_content(request_redis)

    end = time.time()
    result = end - start
    print(result)

    return HTTPException(status_code=status.HTTP_201_CREATED)


# 3시간 이내 데이터 조회
@router.get("/3hours", description="3시간 이내의 데이터를 조회한다.")
async def get_3h_contents():
    start = time.time()
    response = crud_redis.get_3h()
    end = time.time()
    print(end - start)
    return {"data": response}


# 24시간 데이터 조회
@router.get("/today", description="24시간 이내의 데이터를 조회한다.")
async def get_content(db: Session = Depends(get_db)):
    start = time.time()
    response = crud_mysql.get_24h(db)
    end = time.time()
    print(end - start)
    return {"data": response}


@router.get("/count", description="캣타워 데이터의 개수를 반환한다.")
async def get_count_of_data():
    count_response = crud_redis.get_3h_count()
    return count_response


# 테스트

