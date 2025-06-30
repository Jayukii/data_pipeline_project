#	Data Ingestion Pipeline

A FastAPI-powered Python service that ingests live weather data from OpenWeatherMap and stores it securely in PostgreSQL.



## Features

Fetch real-time weather data for any city

Store records in a PostgreSQL database

Secure API key management using .env

RESTful API endpoints with Swagger docs

Modular Python codebase with SQLAlchemy ORM


## Tech Stack

Python 3.11

FastAPI

SQLAlchemy

PostgreSQL

Uvicorn

python-dotenv

## Project Structure
bash

```
data_pipeline_project/
├── app/
│   ├── main.py         # FastAPI entry point
│   ├── ingest.py       # Data fetching logic
│   ├── models.py       # SQLAlchemy models
│   ├── process.py      # Data cleaning/transformation
│   └── utils.py        # Helper functions
├── .env                # Environment variables (not committed)
├── .gitignore
├── requirements.txt
```

## Setup & Installation

1️⃣ Clone the repository
bash
```
git clone https://github.com/YOURUSERNAME/data-ingestion-pipeline.git
cd data-ingestion-pipeline
```
2️⃣ Create a virtual environment
bash
```
python -m venv venv
```
3️⃣ Activate the virtual environment
Windows:

powershell
```
.\venv\Scripts\Activate
```
macOS/Linux:

bash
```
source venv/bin/activate
```
4️⃣ Install dependencies
bash
```
pip install -r requirements.txt
```

5️⃣ Create a .env file
In the project root, create .env:

ini
```
OPENWEATHER_API_KEY=your_real_api_key_here
```

## Important:
Never commit .env to version control.

6️⃣ Configure PostgreSQL
Make sure you have a PostgreSQL server running and create a database, for example weatherdb.

Update DATABASE_URL in main.py if needed:

python
```
DATABASE_URL = "postgresql://postgres:yourpassword@localhost/weatherdb"
```
7️⃣ Run the server
From the project root:

bash
```
uvicorn app.main:app --reload
```
## Your API is live at:

cpp
```
http://127.0.0.1:8000
```
## Swagger docs:

arduino
```
http://127.0.0.1:8000/docs
```
## Example Usage
Ingest Weather Data

bash
```
POST /ingest/{city}
```
Example:

bash
```
POST /ingest/London
```
Retrieve Records

bash
```
GET /records
```

## Future Improvements
Dockerize the application

Add authentication with JWT

Schedule periodic ingestion jobs

Build a frontend dashboard

# License

MIT License
