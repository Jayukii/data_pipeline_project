from pydantic import BaseModel
from datetime import datetime

class WeatherRecordOut(BaseModel):
    id: int
    city: str
    temperature: float
    humidity: int
    description: str
    timestamp: datetime

    # tells Pydantic how to read data from SQLAlchemy models (WeatherRecord) without converting them manually
    class Config:
        from_attributes = True