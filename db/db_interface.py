from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.inspection import inspect
from sqlmodel import Session

from data import config
from logs.config import logger


class DataBaseInterface:

    def __init__(self):
        # self.db_url = config.ENGINE_URL
        self.db_url = config.DATABASE_URL  # for local
        self.engine = create_engine(self.db_url, echo=True)

    def get_session(self) -> Session:
        """
        Creates a session to work with the database
        """
        try:
            session = next(self._create_session())
            return session
        except Exception as e:
            logger.exception(e)
            raise e

    def init_db(self, model):
        """
        Check to exist table
        Creating tables
        :param model: Model for SQL table
        """
        try:
            has_table = inspect(self.engine).has_table(model.__tablename__)
            if not has_table:
                model.metadata.create_all(self.engine)
        except OperationalError as e:
            logger.error(f'Not connection to server for init db')
            raise e

    def _create_session(self):
        with Session(self.engine) as session:
            logger.info('create new session')
            yield session
