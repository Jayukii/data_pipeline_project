import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from models import Base, WeatherRecord
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """Create all tables once before the tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Create a new database session for each test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Create a TestClient with overridden DB dependency."""
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_ingest_weather_data_valid(client):
    mock_data = {"temp": 21, "humidity": 55}
    cleaned_data = {"temperature": 21, "humidity": 55, "city": "london"}

    with patch("main.fetch_weather", return_value=mock_data), \
         patch("main.clean_weather_data", return_value=cleaned_data):
        response = client.post("/ingest/london")
        assert response.status_code == 200
        assert response.json()["status"] == "Data ingested successfully"
        assert response.json()["data"] == cleaned_data

def test_ingest_weather_data_invalid(client):
    mock_data = {"temp": None}
    with patch("main.fetch_weather", return_value=mock_data), \
         patch("main.clean_weather_data", return_value=None):
        response = client.post("/ingest/nowhere")
        assert response.status_code == 200
        assert response.json()["status"] == "Invalid data"

def test_get_records(client, db_session):
    db_session.add(WeatherRecord(temperature=23, humidity=60, city="paris"))
    db_session.commit()

    response = client.get("/records")
    assert response.status_code == 200
    records = response.json()
    assert any(r["city"] == "paris" for r in records)
