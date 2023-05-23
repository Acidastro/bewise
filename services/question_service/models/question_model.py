from sqlmodel import SQLModel, Field


class QuestionBaseModel(SQLModel):
    id_question: int
    text_question: str
    text_answer: str
    date_created: str


class GetQuestionSchema(SQLModel):
    questions_num: int = Field(1, gt=0, le=100)


class QuestionModelTable(QuestionBaseModel, table=True):
    id: int = Field(primary_key=True)
    __tablename__ = 'question'
