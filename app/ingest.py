import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def fetch_weather(city: str):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    return {
        'city': city,
        'timestamp': datetime.utcfromtimestamp(data['dt']),
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity']
    }