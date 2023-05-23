import uuid

from fastapi import UploadFile, Response, HTTPException

from db.db_interface import DataBaseInterface as DBI
from services.audio_service.audio_back import AudioWavFileManager, \
    generate_url
from services.audio_service.audio_db import get_audio_from_db, \
    save_audio_to_db, save_user_to_db, user_is_valid
from services.audio_service.models.audio_model import AudioModelTable
from services.audio_service.models.user_model import UserModelTable, \
    UserUploadSchema, UserSchemaIn


def get_response_for_create_user(user):
    """
    Creates a new session for the database, generates uuid for user,
    creates a user model based on this data.
    The model is saved to the database.
    :param UserSchemaIn user:
    :return: user id , user token
    :rtype: UserUploadSchema
    """
    session = DBI().get_session()
    token = str(uuid.uuid4())
    user = UserModelTable(user_name=user.user_name, user_token=token)
    user = save_user_to_db(user, session)
    return UserUploadSchema(user_id=user.user_id, user_token=token)


def get_response_for_upload_audio(user, file):
    """
    Creates a new session for the database, generates uuid for audio,
    Convert mp3 to wav, create audio model
    The model is saved to the database.
    :param UserUploadSchema user: user id, user token
    :param UploadFile file: wav file
    :return: url for download audio
    """
    session = DBI().get_session()
    if user_is_valid(user, session):
        mp3_file = AudioWavFileManager(file).get_mp3_file()
        token = str(uuid.uuid4())
        audio = AudioModelTable(
            user_id=user.user_id, audio_token=token, audio_file=mp3_file,
        )
        audio_model = save_audio_to_db(audio, session)
        url = generate_url(audio_model.audio_id, audio_model.user_id)
        return Response(content=url, headers={'Content-Type': 'text/plain'})
    raise HTTPException(status_code=404, detail='User not found')


def get_response_for_download_audio(audio_id, user_id) -> Response:
    """
    Creates a new session for the database,
    Gets an audio recording from the database
    :param int audio_id: id uploaded audio
    :param int user_id: id of the user who uploaded the audio.
    :return: audio mp3 file
    :rtype: Response
    """
    try:
        session = DBI().get_session()
        filename = f'{audio_id}_{user_id}.mp3'
        audio_file = get_audio_from_db(audio_id, user_id, session)
        headers = {
            'Content-Disposition': f'attachment;filename={filename}',
            'Content-Type': 'audio/mpeg',
        }
        resp = Response(content=audio_file, headers=headers)
        return resp
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.args[0])
