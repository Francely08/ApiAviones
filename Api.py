from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

app = FastAPI()

SQLALCHEMY_DATABASE_URL = "sqlite:///./airport.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    duration = Column(Integer)

Base.metadata.create_all(bind=engine)

class FlightCreate(BaseModel):
    origin: str
    destination: str
    duration: int
    
    @app.post("/flights/")
    def create_flight(flight: 'FlightCreate'):
     db = SessionLocal()
     db_flight = Flight(origin=flight.origin, destination=flight.destination, duration=flight.duration)
     db.add(db_flight)
     db.commit()
     db.refresh(db_flight)
     return db_flight
    

    @app.get("/flights/{flight_id}")
    def get_flight(flight_id: int):
     db = SessionLocal()
     flight = db.query(Flight).filter(Flight.id == flight_id).first()
     return flight
    
    if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=8000)
    
