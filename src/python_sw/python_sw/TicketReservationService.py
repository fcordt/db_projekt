from datetime import date
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db


class TicketReservationService:
    def __init__(self, connection: Connection = Depends(get_db(autocommit=False))):
        self._connection = connection

    def lock_sitzplatz(connection: Connection, )

    def create_ticket(
            self,
            fahrplan_nr: int, 
            wagon_nr: int, 
            sitzplatznr: int, 
            abfahrt_bahnhof: str, 
            ankunft_bahnhof: str, 
            datum: date):
        with self._connection.cursor() as cursor:

