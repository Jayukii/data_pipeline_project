from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ingest import fetch_weather
from process import clean_weather_data
from models import Base, WeatherRecord

DATABASE_URL = "postgresql://postgres:password@localhost/weatherdb"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/ingest/{city}")
def ingest_weather_data(city: str):
    data = fetch_weather(city)
    cleaned_data = clean_weather_data(data)
    if cleaned_data is None:
        return {"status": "Invalid data"}
    db = SessionLocal()
    record = WeatherRecord(**cleaned_data)
    db.add(record)
    db.commit()
    db.close()
    return {"status": "Data ingested successfully", "data": cleaned_data}

@app.get("/records")
def get_records():
    db = SessionLocal()
    records = db.query(WeatherRecord).all()
    db.close()
    return records