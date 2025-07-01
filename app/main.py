from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from ingest import fetch_weather
from process import clean_weather_data
from models import Base, WeatherRecord
import os
from dotenv import load_dotenv

from typing import List
from schemas import WeatherRecordOut

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/ingest/{city}")
def ingest_weather_data(city: str, db: Session = Depends(get_db)):
    """
    Fetch weather data for a city, clean it, and store it in the database.
    """
    data = fetch_weather(city)
    cleaned_data = clean_weather_data(data)
    if cleaned_data is None:
        return {"status": "Invalid data"}

    record = WeatherRecord(**cleaned_data)
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"status": "Data ingested successfully", "data": cleaned_data}


# FastAPI to serialize the response using WeatherRecordOut
# Automatically documents the schema in Swagger.
@app.get("/records", response_model=List[WeatherRecordOut])
def get_records(db: Session = Depends(get_db)):
    records = db.query(WeatherRecord).all()
    return records
