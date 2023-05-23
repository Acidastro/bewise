from sqlmodel import SQLModel, Field


class UserSchemaIn(SQLModel):
    user_name: str = Field(max_length=20, min_length=2)


class UserUploadSchema(SQLModel):
    user_id: int
    user_token: str


class UserModelTable(UserSchemaIn, table=True):
    user_id: int = Field(default=None, primary_key=True)
    user_token: str = Field(unique=True)
    __tablename__ = 'user'

    class Config:
        arbitrary_types_allowed = True
