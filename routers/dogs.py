from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter
from ..models import Dogs
from ..database import SessionLocal
from starlette import status
from .auth import get_current_owner


router = APIRouter(
    prefix='/dogs',
    tags=['dogs']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
owner_dependency = Annotated[dict, Depends(get_current_owner)]


class BreedEnum(str, Enum):
    french_bulldog = 'French Bulldog'
    labrador_retriever = 'Labrador Retriever'
    golden_retriever = 'Golden Retriever'
    german_shepherd = 'German Shepherd'
    poodle = 'Poodle'
    dashshund = 'Dachshund'
    bulldog = 'Bulldog'
    beagle = 'Beagle'
    rottweiler = 'Rottweiler'
    german_shorthaired_pointer = 'German Shorthaired Pointer'


class TemperamentEnum(str, Enum):
    chill = 'Chill'
    playful = 'Playful'
    aggressive = 'Aggressive'
    anxious = 'Anxious'


class DogRequest(BaseModel):
    dog_name: str = Field(min_length=3)
    temperament: TemperamentEnum = Field(default="Chill")
    description: str = Field(min_length=3, max_length=100)
    breed: BreedEnum = Field(default="Poodle")
    age: int = Field(gt=0, lt=35)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_dogs(owner: owner_dependency, db: db_dependency):
    if not owner:
        raise HTTPException(status_code=401, detail='Not Authorized')
    return db.query(Dogs).filter(Dogs.owner_id == owner.get('id')).all()


@router.get("/{dog_id}", status_code=status.HTTP_200_OK)
async def get_dog_by_id(owner: owner_dependency, db: db_dependency, dog_id: int = Path(gt=0)):
    if not owner:
        raise HTTPException(status_code=401, detail='Not Authorized')
    dog_model = db.query(Dogs).filter(Dogs.owner_id == owner.get('id')).filter(Dogs.id == dog_id).first()
    if not dog_model:
        raise HTTPException(status_code=404, detail='Dog not found')
    return dog_model


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_dog(owner: owner_dependency, db: db_dependency, dog_request: DogRequest):
    if not owner:
        raise HTTPException(status_code=401, detail='Not Authorized')
    dog_model = Dogs(**dog_request.dict(), owner_id=owner.get('id'))

    db.add(dog_model)
    db.commit()


@router.put("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_dog(owner: owner_dependency, db: db_dependency, dog_request: DogRequest, dog_id: int = Path(gt=0)):
    if not owner:
        raise HTTPException(status_code=401, detail='Not Authorized')
    dog_model = db.query(Dogs).filter(Dogs.owner_id == owner.get('id')).filter(Dogs.id == dog_id).first()
    if not dog_model:
        raise HTTPException(status_code=404, detail='Dog not found')
    dog_model.dog_name = dog_request.dog_name
    dog_model.temperament = dog_request.temperament
    dog_model.description = dog_request.description
    dog_model.breed = dog_request.breed
    dog_model.age = dog_request.age

    db.add(dog_model)
    db.commit()


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dog(owner: owner_dependency, db: db_dependency, dog_id: int = Path(gt=0)):
    if not owner:
        raise HTTPException(status_code=401, detail='Not Authorized')
    dog_model = db.query(Dogs).filter(Dogs.owner_id == owner.get('id')).filter(Dogs.id == dog_id).delete()
    if not dog_model:
        raise HTTPException(status_code=404, detail='Dog not found')
    db.commit()

