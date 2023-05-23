from sqlalchemy import select
from sqlalchemy.orm import Session

from logs.config import logger
from services.question_service.models.question_model import QuestionModelTable


def get_all_question_id_from_db(session) -> set:
    """
    Returns all id_questions from db
    :param Session session: session for use db
    :return set: all id_questions from db
    """
    query = select(QuestionModelTable.id_question).select_from(
        QuestionModelTable)
    result = session.execute(query)
    id_list_in_db = {row[0] for row in result}
    return id_list_in_db


def save_questions_in_db(question_list, session):
    """
    :param list question_list: unique question list
    :param Session session: session for use db
    :return:
    """
    for q in question_list:
        session.add(QuestionModelTable(
            id_question=q['id'],
            text_question=q['question'],
            text_answer=q['answer'],
            date_created=q['created_at'],
        ))
    session.commit()
    logger.info(f'saved {len(question_list)} questions')


def get_n_last_questions_from_db(num, session) -> list:
    """
    Getting last n records from db
    :param int num: amount records
    :param Session session: session for use db
    :return list: last n records from db
    """
    query = session.query(QuestionModelTable).order_by(
        QuestionModelTable.id.desc()).limit(num)
    questions = query.all()
    logger.info(f'got {len(questions)} questions from db')
    return questions
