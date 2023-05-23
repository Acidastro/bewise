from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GetQuestionSchema(BaseModel):
    questions_num: int = Field(1, gt=0, le=100)


class QuestionModelTable(Base):
    __tablename__ = 'question'

    id_question = Column(Integer, primary_key=True)
    text_question = Column(String)
    text_answer = Column(String)
    date_created = Column(String)
