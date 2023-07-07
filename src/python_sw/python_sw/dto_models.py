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
    zugnummer: int


class BahnsteigFahrtDTO(BaseModel):
    id: int
    bahnhof_name: str
    bahnsteig_nr: int
    uhrzeit: datetime

class BahnsteigFahrtInsertDTO(BaseModel):
    bahnhof_name: str
    bahnsteig_nr: int
    uhrzeit: datetime


class FahplanStopDTO(BaseModel):
    abfahrt: Optional[BahnsteigFahrtDTO]
    ankunft: Optional[BahnsteigFahrtDTO]

class UserDTO(BaseModel):
    vorname: str
    nachname: str
    kundennummer: str
    adresse: str
    plz: str
    ort: str

class WagonDTO(BaseModel):
    wagontyp: str
    klasse: int
    freie_sitze: list[int]

class ZugDTO(BaseModel):
    name: str
    zugnummer: int
    zugtyp: str
    wagen: list[WagonDTO]
