from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class AudioModelTable(Base):
    __tablename__ = 'audio'
    audio_id = Column(Integer, default=None, primary_key=True)
    user_id = Column(Integer, )
    audio_token = Column(String, unique=True)
    audio_file = Column(String, )
