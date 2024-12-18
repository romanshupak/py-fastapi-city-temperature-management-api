from datetime import datetime

import requests
from sqlalchemy.orm import Session
from City_CRUD_API.models import City
from Temperature_API import models
from Temperature_API.models import Temperature
from Temperature_API.schemas import TemperatureCreate


WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
API_KEY = "d0eae92abc5b4efaa76144848242007"


def get_all_temperatures(db: Session):
    return db.query(models.Temperature).all()


def get_temperature_by_city(db: Session, city_id: int):
    return (
        db.query(models.Temperature)
        .filter(models.Temperature.city_id == city_id).all()
    )


# Update temperature for all cities
def update_temperatures(db: Session):
    cities = db.query(City).all()
    for city in cities:
        try:
            # Request to Weather API
            response = requests.get(
                WEATHER_API_URL,
                params={"key": API_KEY, "q": city.name}
            )
            # Check response status
            if response.status_code == 200:
                data = response.json()
                temp = data["current"]["temp_c"]  # Temp in JSON response

                # Create new record in Data Base
                db_temp = Temperature(
                    date_time=datetime.utcnow(),
                    temperature=temp,
                    city_id=city.id
                )
                db.add(db_temp)
            else:
                print(
                    f"Failed to fetch data for city"
                    f" {city.name}: {response.status_code}"
                )
        except Exception as e:
            print(f"Error fetching data for city {city.name}: {e}")

    # One commit after handle all cities
    db.commit()
    return {"message": "Temperatures updated successfully"}


# Create a new temperature record
def create_temperatures(db: Session, temperatures: TemperatureCreate):
    db_temp = Temperature(
        date_time=temperatures.date_time,
        temperature=temperatures.temperature,
    )
    db.add(db_temp)
    db.commit()
    db.refresh(db_temp)
    return db_temp


# Get temperature by ID
def get_temperature_by_id(db: Session, temp_id: int):
    return db.query(Temperature).filter(Temperature.id == temp_id).first()
