from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Owners(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Dogs(Base):
    __tablename__ = 'dogs'

    id = Column(Integer, primary_key=True, index=True)
    dog_name = Column(String)
    temperament = Column(String)
    description = Column(String)
    breed = Column(String)
    age = Column(Integer)
    owner_id = Column(Integer, ForeignKey("owners.id"))

