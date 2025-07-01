from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class WeatherRecord(Base):
    __tablename__ = 'weather_records'

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)