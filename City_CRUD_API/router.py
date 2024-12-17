from fastapi import FastAPI, Depends, HTTPException, Query, APIRouter
from sqlalchemy.orm import Session

from . import schemas, crud
from database import SessionLocal
from dependencies import get_db

router = APIRouter()


# Retrieve a list of all cities
@router.get("/cities/", response_model=list[schemas.CityList])
def read_cities(db: Session = Depends(get_db)):
    return crud.get_all_cities(db=db)


# Get the details of a specific city by ID
@router.get("/cities/{city_id}/", response_model=schemas.CityList)
def read_city(city_id: int, db: Session = Depends(get_db)):
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


# Create a new city
@router.post("/cities/", response_model=schemas.CityList)
def create_city(
        city: schemas.CityCreate,
        db: Session = Depends(get_db),
):
    db_city = crud.get_city_by_name(db=db, name=city.name)

    if db_city:
        raise HTTPException(
            status_code=400,
            detail="Such name for City already exists"
        )

    return crud.create_city(db=db, city=city)


# Update the details of a specific city
@router.put("/cities/{city_id}/", response_model=schemas.CityList)
def update_city(
        city_id: int,
        city_update: schemas.CityUpdate,
        db: Session = Depends(get_db),
):
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")

    updated_city = crud.update_city(
        db=db,
        city_id=city_id,
        name=city_update.name,
        additional_info=city_update.additional_info,
    )
    return updated_city


# Delete a specific city
@router.delete("/cities/{city_id}/", response_model=schemas.CityList)
def delete_city(
        city_id: int,
        db: Session = Depends(get_db),
):
    city = crud.get_city_by_id(db=db, city_id=city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return crud.delete_city(db=db, city_id=city_id)
