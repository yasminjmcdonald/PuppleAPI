from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter
from ..models import Owners
from ..database import SessionLocal
from starlette import status
from passlib.context import CryptContext
from .auth import get_current_owner


router = APIRouter(
    prefix='/owners',
    tags=['owners']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
owner_dependency = Annotated[dict, Depends(get_current_owner)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class OwnerVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_owner(owner: owner_dependency, db: db_dependency):
    if owner is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Owners).filter(Owners.id == owner.get('id')).first()


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(owner: owner_dependency, db: db_dependency, owner_verification: OwnerVerification):
    if owner is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    owner_model = db.query(Owners).filter(Owners.id == owner.get('id')).first()
    if not bcrypt_context.verify(owner_verification.password, owner_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    owner_model.hashed_password = bcrypt_context.hash(owner_verification.new_password)

    db.add(owner_model)
    db.commit()

