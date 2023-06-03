from typing import Optional
from fastapi import Depends, FastAPI

from python_sw.BahnhofService import BahnhofService
from python_sw.FahplanService import FahrplanService

app = FastAPI()


@app.get("/api/v1/stations")
def get_bahnhof(name: Optional[str] = "", bahnhof_service: BahnhofService = Depends()):
    return bahnhof_service.get_stations(name)


@app.get("/api/v1/schedule")
def get_fahrplan(fahrplan_service: FahrplanService = Depends()):
    return fahrplan_service.get_fahrplaene()


@app.get("/api/v1/schedule/{nr}")
def get_fahrplan(nr: int, fahrplan_service: FahrplanService = Depends()):
    return fahrplan_service.get_fahrplan_details(nr)
