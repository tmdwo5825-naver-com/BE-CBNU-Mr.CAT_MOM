from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. common.dependencies import get_db
from .. import schemas, crud

from .. aws.s3 import upload_file, create_presigned_url


router = APIRouter()


@router.post("/content-create/", description="file upload 및 db에 content 추가.")
def create_content(request: schemas.CatCreate, db: Session = Depends(get_db)):
    if not request.image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )
    obj_name = upload_file(request.image)
    crud.create_cat(db, request, obj_name)


@router.get("/", response_model= list[schemas.CatResponse], description="db의 record를 읽어온다.")
def get_content(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    response: schemas.CatResponse = crud.get_cat(db=db, skip=skip, limit=limit)
    if response is None:
        raise HTTPException(status_code=404, detail= "content not found")
    for i in response:
        response.url = create_presigned_url('s3', response.obj_name)

    return response
