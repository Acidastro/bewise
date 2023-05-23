import base64

from sqlalchemy.orm import Session

from logs.config import logger
from services.audio_service.models.audio_model import AudioModelTable
from services.audio_service.models.user_model import UserModelTable, \
    UserUploadSchema


def save_user_to_db(user, session) -> UserModelTable:
    """
    Saves the user model to the database
    :param UserModelTable user:
    :param Session session: SQLAlchemy session
    """
    try:
        session.add(user)
        session.commit()
        logger.info(f'user "{user.user_name}" successfully saved in db')
        return user
    except Exception as e:
        logger.exception(e)
        raise e


def save_audio_to_db(audio, session) -> AudioModelTable:
    """
    Saves the audio model to the database
    :param AudioModelTable audio:
    :param Session session: SQLAlchemy session
    :return: AudioModel
    """
    try:
        session.add(audio)
        session.commit()
        logger.info(
            f'audio of user id: "{audio.user_id}" successfully saved in db')
        return audio
    except Exception as e:
        logger.exception(e)
        raise e


def get_audio_from_db(audio_id, user_id, session) -> bytes:
    """
    Get audio from db, decode, convert to mp3
    :param int user_id:
    :param int audio_id:
    :param Session session: SQLAlchemy session
    :return: audio file bytes format
    """
    try:
        audio_model = session.query(AudioModelTable).filter(
            AudioModelTable.audio_id == audio_id,
            AudioModelTable.user_id == user_id,
        ).first()

        if audio_model is not None:
            audio_bytes = base64.b64decode(audio_model.audio_file)  # decode
            return audio_bytes
        raise FileNotFoundError(
            f'File for user id={user_id} audio id={audio_id} is not found!'
        )
    except Exception as e:
        logger.exception(e)
        raise e


def user_is_valid(user, session) -> bool:
    """
    Check user in db
    :param UserUploadSchema user:
    :param Session session: SQLAlchemy session
    :return bool: True if user else False
    """
    try:
        user_model = session.query(UserModelTable).filter(
            UserModelTable.user_id == user.user_id,
            UserModelTable.user_token == user.user_token,
        ).first()
        return user_model is not None
    except Exception as e:
        logger.exception(e)
        raise e
