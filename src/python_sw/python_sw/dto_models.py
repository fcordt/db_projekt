from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class TrainStationDTO(BaseModel):
    name: str
    adresse: Optional[str]
    plz: str
    ort: str
    bahnsteige: int


class FahrplanDTO(BaseModel):
    nr: int
    name: str
    von: datetime
    bis: datetime


class BahnsteigFahrtDTO(BaseModel):
    bahnhof_name: str
    bahnsteig_nr: int
    uhrzeit: datetime


class FahplanStopDTO(BaseModel):
    abfahrt: Optional[BahnsteigFahrtDTO]
    ankunft: Optional[BahnsteigFahrtDTO]
