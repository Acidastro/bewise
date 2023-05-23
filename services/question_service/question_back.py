import json

import requests
from sqlalchemy.orm import Session

from data import config
from logs.config import logger
from services.question_service.question_db import get_all_question_id_from_db, \
    save_questions_in_db, \
    get_n_last_questions_from_db


class QuestionInterface:

    def __init__(self, session):
        """
        :param Session session: SQLAlchemy session
        """
        self.session = session

    def get_question_from_db(self) -> str:
        """
        Ответом на запрос должен быть предыдущей сохранённый вопрос для викторины.
        В случае его отсутствия - пустой объект.
        """
        try:
            resp = get_n_last_questions_from_db(1, self.session)
            if len(resp) > 0:
                resp = resp[0].text_question
            return resp
        except Exception as e:
            logger.error(e)
            raise e

    def save_request_to_db(self, num):
        """
        Sends a request, processes and saves to db.
        :param int num: number of questions
        """
        # get response
        resp_question_list = self._send_request_for_question_api(num)
        # check for duplicated
        uniq_id_in_resp = self._find_unique_question_id(resp_question_list)
        amount_duplicated = len(resp_question_list) - len(uniq_id_in_resp)
        if len(uniq_id_in_resp) > 0:  # save uniq question set
            uniq_resp = self._find_unique_dict(uniq_id_in_resp,
                                               resp_question_list)
            save_questions_in_db(uniq_resp, self.session)
        if amount_duplicated > 0:  # if duplicates, recursion
            self.save_request_to_db(amount_duplicated)

    @staticmethod
    def _send_request_for_question_api(num: int) -> list:
        """
        Send a request for api question
        :param int num: amount questions
        :return list: response list from request
        """
        path = config.API_QUESTION_REQUEST_PATH
        resp = requests.get(f'{path}{num}')
        logger.info(f'response STATUS {resp.status_code}')
        resp_list = json.loads(resp.text)
        logger.info(f'got {len(resp_list)} questions from response')
        return resp_list

    def _find_unique_question_id(self, resp_list) -> set:
        """
        Find unique id set of response
        :param list resp_list:
        :return set: unique id set of response
        """
        id_in_resp = {resp['id'] for resp in resp_list}
        id_in_db = get_all_question_id_from_db(self.session)

        uniq_id_in_resp = {r for r in id_in_resp if r not in id_in_db}
        logger.info(f'amount unique id = {len(uniq_id_in_resp)}')
        return uniq_id_in_resp

    @staticmethod
    def _find_unique_dict(set_id, resp_list) -> list:
        """
        Find unique dicts of response
        :param set_id: unique id set of response
        :param list resp_list: list of dicts
        :return list: unique dicts of response
        """
        uniq_resp = [r for r in resp_list if r['id'] in set_id]
        return uniq_resp
