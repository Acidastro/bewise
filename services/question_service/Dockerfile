FROM python:3.10

COPY ./services/question_service/requirements.txt .

RUN pip install -r requirements.txt

COPY ./data /data
COPY ./logs/config.py /logs/config.py
COPY ./services/question_service /services/question_service
COPY ./db/db_interface.py /db/db_interface.py
