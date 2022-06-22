import pytest
from app import app, get_trip_weather

def test_function_exists():
    with app.app_context():
        result = get_trip_weather("seattle", 1656220067, 1656306467)
        assert result