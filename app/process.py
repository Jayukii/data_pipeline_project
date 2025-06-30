def clean_weather_data(record):
    if record["temperature"] is None or record["humidity"] is None:
        return None
    return record