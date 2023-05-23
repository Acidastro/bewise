import base64
from io import BytesIO

from fastapi import UploadFile, HTTPException
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError

from data.config import POSTGRES_HOST, WEB_PORT
from logs.config import logger


def generate_url(audio_id, user_id) -> str:
    """
    :return: Возвращает URL для скачивания записи вида
    http://host:port/record?id=id_записи&user=id_пользователя
    """
    url = f'http://{POSTGRES_HOST}:23001' \
          f'/record?audio={audio_id}&user={user_id}'
    return url


class AudioWavFileManager:
    def __init__(self, audio_file):
        """
        Reads a file, converts to mp3 format, encode to base64
        :param UploadFile audio_file: only wav
        """
        self.wav_file = self._read_audio_file(audio_file)

    def get_mp3_file(self) -> str:
        """
        Get ready mp3 file in base64 format
        :return: mp3 file base64 format  for save to database
        """
        try:
            mp3_file_bytes = self._convert_wav_to_mp3(self.wav_file).getvalue()
            mp3_file = self._encode_audio_to_base64(mp3_file_bytes)
            return mp3_file
        except CouldntDecodeError as e:
            logger.error(f'Invalid .wav file!')
            raise HTTPException(status_code=400, detail='Invalid .wav file!')

    @staticmethod
    def _read_audio_file(audio_file) -> BytesIO:
        """
        Read .wav audio file in bytes
        :param UploadFile audio_file: file from faspApi upload
        :return bytes:
        """
        if audio_file.filename.endswith(".wav"):
            wav_file = audio_file.file.read()
            if len(wav_file) == 0:
                raise HTTPException(status_code=400, detail='.wav file is empty')
            wav_file = BytesIO(wav_file)
            return wav_file
        raise HTTPException(status_code=400, detail="Invalid audio format. Only .WAV is supported")

    @staticmethod
    def _convert_wav_to_mp3(file) -> BytesIO:
        """
        Convert to mp3 file from .wav file
        :param BytesIO file: .wav file
        :return: BytesIO mp3_file
        """
        mp3_file = AudioSegment.from_wav(file).export(BytesIO(), format="mp3")
        return mp3_file

    @staticmethod
    def _encode_audio_to_base64(file) -> str:
        """
        Encode format for database
        :param bytes file:
        :return: base64 format decode
        """
        audio_base64 = base64.b64encode(file).decode('utf-8')
        return audio_base64
