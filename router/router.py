from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi import File, UploadFile
from sqlalchemy.orm import Session
from typing import IO

from .. import models
from .. database.set_mysql import engine


from .. common.dependencies import get_db
from .. import schemas, crud

from .. aws.s3 import upload_file, create_presigned_url


from ..core.config import settings

models.Base.metadata.create_all(bind = engine)

router = APIRouter()



@router.post("/content-create/", description="file upload 및 db에 content 추가.")
async def create_content(
        comment: str = Form(),
        x: int = Form(),
        y: int = Form(),
        image: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    if not image:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No image found"
        )


@router.get("/", response_model= list[schemas.CatResponse], description="db의 record를 읽어온다.")
def get_content(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    response: schemas.CatResponse = crud.get_cat(db=db, skip=0, limit=0)
    if response is None:
        raise HTTPException(status_code=404, detail= "content not found")
    for i in response:
        response.url = create_presigned_url('s3', response.obj_name)

    return response
