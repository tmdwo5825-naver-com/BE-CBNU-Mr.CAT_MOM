from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi import File, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.crud.crud_cat import crud_cat
from app.aws.s3 import upload_file
from app.core.config import settings
from app.database.set_mysql import engine
from app.api.deps import save_file, check_location, get_db, process_image


models.Base.metadata.create_all(bind=engine)

router = APIRouter()


@router.post("/content-create/", description="file upload 및 mysql db,redis db에 content 추가.")
async def create_content(
        comment: str = Form(default=None, description="사진에 추가할 코멘트"),
        x: float = Form(description="float형 경도"),
        y: float = Form(description="위도"),
        image: UploadFile = File(description="클라이언트가 업로드할 이미지, 이미지 형식은 미정(아직은 jpeg만 처리한다.)"),
        db: Session = Depends(get_db)
):
    print(image.filename)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )

    # 파일 처리 부분
    path = await save_file(image.file)
    file_info = process_image(path) # 처리된 파일의 경로 및 컨텐츠 타입 반환

    # 파일 s3에 업로드
    obj_name = upload_file(file_info[0], file_info[1])
    image_url = f'https://{settings.s3_bucket_name}.s3.{settings.s3_location}.amazonaws.com/{obj_name}'

    # 객체 처리
    cat_tower = check_location(x, y)
    request = schemas.CatCreate(comment=comment, image_url=image_url, x=x, y=y, cat_tower=cat_tower)

    # db 저장
    crud_cat.create_24h_content(db, request)

    # redis 저장
    crud_cat.create_3h_content(request)

    return HTTPException(status_code=status.HTTP_201_CREATED)


# 3시간 이내 데이터 조회
@router.get("/3hours", description="3시간 이내의 데이터를 조회한다.")
def get_3h_contents():
    response = crud_cat.get_3h()

    return {"data": response}


# 24시간 데이터 조회
@router.get("/today", description="24시간 이내의 데이터를 조회한다.")
def get_content(db: Session = Depends(get_db)):
    response = crud_cat.get_24h(db)
    return {"data": response}

# 테스트
@router.post("/test", description="테스트를 위한 api")
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


    # print(cat_tower)
    request = schemas.CatCreate(comment=comment, image_url=image_url, x=x, y=y, cat_tower=cat_tower)

    crud_cat.create_3h_content(request)
    return HTTPException(status_code=status.HTTP_201_CREATED)
    # request_json = test(comment=request.comment, url=request.image_url)
    #print(request_json)
    #json_str = str(json_form)

    #r = get_redis()
    #r.execute_command("JSON.SET", 'item'+request.image_url, '.', json.dumps(json_form))


# 테스트
@router.get("/test/get", description="test를 위한 api")
def get(db: Session = Depends(get_db)):
    recent_data = crud_cat.get_24h(db)
    return recent_data

