from pydantic import BaseModel, Field
from sqlalchemy import Column, String, Integer

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserSchemaIn(BaseModel):
    user_name: str = Field(max_length=20, min_length=2)


class UserUploadSchema(BaseModel):
    user_id: int
    user_token: str


class UserModelTable(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True)
    user_token = Column(String)
    user_name = Column(String)
