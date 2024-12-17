from sqlalchemy.orm import Session

from City_CRUD_API import models
from City_CRUD_API.schemas import CityCreate


def get_all_cities(db: Session):
    return db.query(models.City).all()


def create_city(db: Session, city: CityCreate):
    db_city = models.City(
        name=city.name,
        additional_info=city.additional_info,
    )
    db.add(db_city)
    db.commit()
    db.refresh(db_city)

    return db_city


def get_city_by_id(db: Session, city_id: int):
    return (
        db.query(models.City).
        filter(models.City.id == city_id).first()
    )


def get_city_by_name(db: Session, name: str):
    """
    In case the same city already exists
    """
    return (
        db.query(models.City).filter(models.City.name == name).first()
    )


def update_city(
        db: Session,
        city_id: int,
        name: str = None,
        additional_info: str = None,
):
    city = get_city_by_id(db, city_id)
    if name:
        city.name = name
    if additional_info:
        city.additional_info = additional_info
    db.commit()
    db.refresh(city)
    return city


def delete_city(db: Session, city_id: int):
    city = get_city_by_id(db, city_id)
    db.delete(city)
    db.commit()
    return {"detail": f"City with ID {city_id} deleted successfully."}
