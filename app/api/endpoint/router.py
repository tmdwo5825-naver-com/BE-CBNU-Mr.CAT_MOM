from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas

from app.common.dependencies import get_db
from app.crud.crud_cat import crud_cat
from app.aws.s3 import upload_file
from app.core.config import settings
from app.database.set_mysql import engine
from app.api.deps import save_file, check_location
from app.database.set_redis import get_redis


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/content-create/", description="file upload 및 db에 content 추가.")
async def create_content(
        comment: str = Form(default=None, description="사진에 추가할 코멘트"),
        x: float = Form(description="float형 경도"),
        y: float = Form(description="위도"),
        image: UploadFile = File(description="클라이언트가 업로드할 이미지, 이미지 형식은 미정(아직은 jpeg만 처리한다.)"),
        db: Session = Depends(get_db)
):
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )

    # 파일 처리 부분
    path = await save_file(image.file)
    obj_name = upload_file(path)

    image_url = f'https://{settings.s3_bucket_name}.s3.{settings.s3_location}.amazonaws.com/{obj_name}'

    # 객체 처리
    cat_tower = check_location(x, y)
    request = schemas.CatCreate(comment=comment, image_url=image_url, x=x, y=y, cat_tower=cat_tower)

    # db 저장
    crud_cat.create_24h_content(db, request)

    # redis 저장
    crud_cat.create_3h_content(request)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get("/") #response_model= list[schemas.CatResponse], description="3시간 이내의 데이터를 조회한다."
def get_3h_contents():
    r = get_redis()
    crud_cat.get_3h()
    # response = crud_cat.get_3h()

    # raise HTTPException(status_code=status.HTTP_200_OK)
    # return response




@router.post("/test")
async def create_content(
        comment: str = Form(default=None, description="사진에 추가할 코멘트"),
        x: float = Form(description="float형 경도"),
        y: float = Form(description="위도"),
        image: UploadFile = File(description="클라이언트가 업로드할 이미지, 이미지 형식은 미정(아직은 jpeg만 처리한다.)"),
        db: Session = Depends(get_db)
):

    # 파일 처리 부분
    path = await save_file(image.file)
    obj_name = upload_file(path)

    image_url = f'https://{settings.s3_bucket_name}.s3.{settings.s3_location}.amazonaws.com/{obj_name}'

    # 객체 처리
    cat_tower = check_location(x, y)
    print(cat_tower)
    request = schemas.CatCreate(comment=comment, image_url=image_url, x=x, y=y, cat_tower=cat_tower)
    # request_json = test(comment=request.comment, url=request.image_url)
    #print(request_json)
    #json_str = str(json_form)

    #r = get_redis()
    #r.execute_command("JSON.SET", 'item'+request.image_url, '.', json.dumps(json_form))



@router.get("/test/get")
def get():
    response = []
    data = schemas.CatResponse(x=36.65, y=34.566, image_url="alsdkjf", comment="asdf")
    response.append(data)
    return {data: response}






# 3시간 데이터 조회
@router.get("/today", response_model= list[schemas.CatResponse])
def get_content(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    response: schemas.CatResponse = crud_cat.get_24h(db, skip, limit)
    if response is None:
        raise HTTPException(status_code=404, detail= "content not found")

    return response
