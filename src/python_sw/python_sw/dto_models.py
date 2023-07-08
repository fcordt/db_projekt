from datetime import date, datetime
from decimal import Decimal
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
    bahnhof_name: str
    bahnsteig_nr: int
    uhrzeit: datetime

class BahnsteigFahrtInsertDTO(BaseModel):
    bahnhof_name: str
    bahnsteig_nr: int
    uhrzeit: datetime


class FahplanStopDTO(BaseModel):
    id: int
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
    wagonnummer: int
    wagontyp: str
    klasse: int
    freie_sitze: list[int]

class ZugDTO(BaseModel):
    name: str
    zugnummer: int
    zugtyp: str
    wagen: list[WagonDTO]

class TicketPreisDTO(BaseModel):
    anzahl_stationen: int
    preis_je_station: float
    ticketpreis: float
    reservierungsaufschlag: float
    gesamtkosten: float

class TicketDTO(BaseModel):
    ticket_nr: int