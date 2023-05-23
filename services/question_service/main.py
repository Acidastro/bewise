import uvicorn
from fastapi import FastAPI

from db.db_interface import DataBaseInterface as DBI
from services.question_service.models.question_model import GetQuestionSchema, \
    QuestionModelTable
from services.question_service.question_back import QuestionInterface

app = FastAPI()
DBI().init_db(QuestionModelTable)


@app.post('/get_question/')
async def get_question(data: GetQuestionSchema):
    session = DBI().get_session()
    question_manager = QuestionInterface(session)
    num = data.questions_num
    resp = question_manager.get_question_from_db()
    question_manager.save_request_to_db(num)
    return resp


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
