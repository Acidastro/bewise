import uvicorn
from fastapi import FastAPI, UploadFile, File, Response, Depends

from db.db_interface import DataBaseInterface as DBI
from services.audio_service.models.audio_model import AudioModelTable
from services.audio_service.models.user_model import UserSchemaIn, \
    UserUploadSchema, UserModelTable
from services.audio_service.views import get_response_for_upload_audio, \
    get_response_for_download_audio, get_response_for_create_user

app = FastAPI()


@app.on_event("startup")
def startup_event():
    """
    Creates all the required tables
    """
    db_interface = DBI()
    models = [UserModelTable, AudioModelTable]
    for model in models:
        db_interface.init_db(model)


@app.post('/create_user/', response_model=UserUploadSchema)
async def create_user(user: UserSchemaIn):
    """
    Создаёт в базе данных пользователя заданным именем,
    так же генерирует уникальный идентификатор пользователя
    и UUID токен доступа (в виде строки) для данного пользователя;
    :param user: запросы с именем пользователя
    :return: Возвращает сгенерированные идентификатор пользователя и токен.
    """
    resp = get_response_for_create_user(user)
    return resp


@app.post('/upload_audio/')
async def upload_audio(
        user: UserUploadSchema = Depends(),
        file: UploadFile = File(..., media_type="audio/wav"),
) -> Response:
    """
    Принимает на вход запросы, содержащие уникальный идентификатор пользователя,
    токен доступа и аудиозапись в формате wav;

    Преобразует аудиозапись в формат mp3,
    генерирует для неё уникальный UUID идентификатор
    и сохраняет их в базе данных;
    :return: URL для скачивания записи вида
    http://host:port/record?id=id_записи&user=id_пользователя
    """
    resp = get_response_for_upload_audio(user, file)
    return resp


@app.get('/record/')
async def download_audio(audio: int,
                         user: int,
                         ) -> Response:
    """
    Предоставляет возможность скачать аудиозапись по ссылке вида
    http://host:port/record?id=id_записи&user=id_пользователя
    :param int audio: audio_id from db
    :param int user: user_id from db
    :return: mp3 audio file
    """
    resp = get_response_for_download_audio(audio, user)
    return resp


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=23001)
