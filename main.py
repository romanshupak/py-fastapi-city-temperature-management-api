from fastapi import FastAPI
from sqlalchemy.orm import Session

from City_CRUD_API import router as city_router
from database import SessionLocal

app = FastAPI()

app.include_router(city_router.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
