FROM python:3.10

COPY ./services/audio_service/requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update
RUN apt-get install -y ffmpeg

COPY ./data/ /data
COPY ./logs/config.py /logs/config.py
COPY ./services/audio_service /services/audio_service
COPY ./db/db_interface.py /db/db_interface.py
RUN chmod +x ./data/wait-for-it.sh
