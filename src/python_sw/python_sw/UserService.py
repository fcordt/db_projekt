import logging
from fastapi import Depends, HTTPException
from oracledb import Connection, DatabaseError

from python_sw.DbService import get_db_service
from python_sw.dto_models import BahnsteigFahrtDTO, FahplanStopDTO, FahrplanDTO, UserDTO

logger = logging.getLogger(__name__) 

class UserService:
    def __init__(self, connection: Connection = Depends(get_db_service)):
        self._connection = connection

    def get_users(
        self,
        vorname: str = None,
        nachname: str = None,
        adresse: str = None,
        plz: str = None,
        ort: str = None,
    ):
        with self._connection.cursor() as cursor:
            select = "SELECT KUNDENNUMMER, VORNAME, NACHNAME, ADRESSE, PLZ, NAME FROM KUNDIN INNER JOIN ORT ON PLZ = ORT_PLZ"
            bvar = []
            if vorname != None:
                select += " WHERE VORNAME LIKE :vn"
                bvar.append("%" + vorname + "%")
            if nachname != None:
                select += " WHERE NACHNAME LIKE :nn"
                bvar.append("%" + nachname + "%")
            if adresse != None:
                select += " WHERE ADRESSE LIKE :adr"
                bvar.append("%" + adresse + "%")
            if plz != None:
                select += " WHERE PLZ LIKE :plz"
                bvar.append("%" + plz + "%")
            if ort != None:
                select += " WHERE NAME LIKE :ort"
                bvar.append("%" + ort + "%")
            return list(
                map(
                    lambda x: UserDTO(kundennummer=x[0], vorname=x[1], nachname=x[2], adresse=x[3], plz=x[4], ort=x[5]),
                    cursor.execute(
                        select, bvar
                    )
                )
            )

    def get_user_by_kundennummer(
        self, kundennummer: str
    ):
        with self._connection.cursor() as cursor:
            x = cursor.execute(
                        "SELECT KUNDENNUMMER, VORNAME, NACHNAME, ADRESSE, PLZ, NAME FROM KUNDIN INNER JOIN ORT ON PLZ = ORT_PLZ WHERE KUNDENNUMMER = :knr",
                        knr=kundennummer
                    ).fetchone()
            if x is None:
                raise HTTPException(status_code=404, detail="Benutzer nicht vorhanden")
            return UserDTO(kundennummer=x[0], vorname=x[1], nachname=x[2], adresse=x[3], plz=x[4], ort=x[5])

    def insert_kunde(self, kundennummer: str, vorname: str, nachname: str, adresse: str, plz: str):
        with self._connection.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO KUNDIN(KUNDENNUMMER, VORNAME, NACHNAME, ADRESSE, ORT_PLZ) VALUES (:nr, :vn, :nn, :adr, :plz)",
                    nr=kundennummer,
                    vn=vorname,
                    nn=nachname,
                    adr=adresse,
                    plz=plz
                )
            except DatabaseError:
                raise HTTPException(status_code=404, detail="Ort nicht gefunden")

    def update_kunde(self, kundennummer: str, vorname: str, nachname: str, adresse: str, plz: str):
        with self._connection.cursor() as cursor:
            try:
                cursor.execute(
                    "UPDATE KUNDIN SET VORNAME=:vn, NACHNAME=:nn, ADRESSE=:adr, ORT_PLZ=:plz WHERE KUNDENNUMMER = :nr",
                    nr=kundennummer,
                    vn=vorname,
                    nn=nachname,
                    adr=adresse,
                    plz=plz
                )
            except DatabaseError as e:
                raise HTTPException(status_code=404, detail=f"Kunde Existiert nicht: {e}")

    def delete_kunde(self, kundennummer: str):
        with self._connection.cursor() as cursor:
            try:
                cursor.execute(
                    "DELETE FROM KUNDIN WHERE KUNDENNUMMER = :nr",
                    nr=kundennummer,
                )
            except DatabaseError:
                raise HTTPException(status_code=404, detail="Kunde Existiert nicht!!!!1111")