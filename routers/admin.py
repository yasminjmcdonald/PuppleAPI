from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter
from models import Dogs
from database import SessionLocal
from starlette import status
from .auth import get_current_owner

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
owner_dependency = Annotated[dict, Depends(get_current_owner)]


@router.get("/dogs", status_code=status.HTTP_200_OK)
async def read_all(owner: owner_dependency, db: db_dependency):
    if owner is None or owner.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Dogs).all()


@router.delete("/dogs/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(owner: owner_dependency, db: db_dependency, dog_id: int = Path(gt=0)):
    if owner is None or owner.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Dogs).filter(Dogs.id == dog_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Dogs).filter(Dogs.id == dog_id).delete()

    db.commit()
