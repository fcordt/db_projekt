from datetime import date
from fastapi import Depends, HTTPException
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.FreePlaceService import FreePlaceService
from python_sw.dto_models import TicketDTO


class TicketReservationService:
    def __init__(self, connection: Connection = Depends(get_db(autocommit=False))):
        self._connection = connection

    def _lock_sitzplatz(self, sitzplatznr: int, wagonnr: int, fahrplannummer: int):
        with self._connection.cursor() as cursor:
            cursor.execute(
                        """
                        SELECT * FROM SITZPLATZ 
                        INNER JOIN FAHRPLAN
                        ON FAHRPLAN.ZUG_ZUGNUMMER = SITZPLATZ.WAGIN_ZUGNUMMER
                        WHERE SITZPLATZNUMMER = :spnr AND FAHRPLAN.NR = :fpnr AND WAGON_REIHENFOLGE = :rf
                        FOR UPDATE
                        """,
                        [sitzplatznr, fahrplannummer, wagonnr])
            
    def _get_zugnr(self, fahrplan_nr : int, datum: date):
        with self._connection.cursor() as cursor:
            for row in cursor.execute("SELECT ZUG_ZUGNUMMER FROM FAHRPLAN WHERE NR = :fpn AND :dt BETWEEN VON_DATUM AND BIS_DATUM",
                                      [fahrplan_nr, datum]):
                return row[0]
            
    def _get_ticketnr(self):
        with self._connection.cursor() as cursor:
            for row in cursor.execute("SELECT ticket_seq.NEXTVAL FROM DUAL"):
                return row[0]
            
    def _create_ticket(self, ticket_nr: int, typ: str, datum: date):
        with self._connection.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO TICKET(TICKETNR, GÜLTIGKEITSDATUM, TICKET_TYP)
                    VALUES(:nr, :dat, :typ)
                """, [ticket_nr, typ, datum])

    def _insert_ticket(
            self,
            datum: date,
            fahrplan_nr: int,
            abfahrt_bahnhof: str,
            ankunft_bahnhof: str,
            wagon_nr: int,
            sitzplatz_nr: int
    ):
        abfahrt_bahnsteig, ankunft_bahnsteig = self._get_bahnsteige(fahrplan_nr, abfahrt_bahnhof, ankunft_bahnhof)
        zug_nr = self._get_zugnr(fahrplan_nr, datum)
        ticket_nr = self._get_ticketnr()
        self._create_ticket(ticket_nr, 'EINZELTICKET', datum)
        self._create_einzelticket(ticket_nr, abfahrt_bahnhof, abfahrt_bahnsteig, ankunft_bahnhof, ankunft_bahnsteig)
        self._create_einzelticket_mit_spr(ticket_nr, sitzplatz_nr, wagon_nr, zug_nr)
        return ticket_nr


    def create_ticket(
            self,
            fahrplan_nr: int, 
            wagon_nr: int, 
            sitzplatznr: int, 
            abfahrt_bahnhof: str, 
            ankunft_bahnhof: str, 
            datum: date) -> TicketDTO:
        self._lock_sitzplatz(sitzplatznr, wagon_nr, fahrplan_nr)
        free_places = FreePlaceService(self._connection).get_free_tickets(fahrplan_nr, abfahrt_bahnhof, ankunft_bahnhof, datum, wagon_nr)
        if sitzplatznr not in free_places:
            raise HTTPException(status_code=404, detail="Ticket bereits vergeben")
        
        ticket_nr = self._insert_ticket(datum, fahrplan_nr, abfahrt_bahnhof, ankunft_bahnhof, wagon_nr, sitzplatznr)
        return TicketDTO(ticket_nr=ticket_nr)


