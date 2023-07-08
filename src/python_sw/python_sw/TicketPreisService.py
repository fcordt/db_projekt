from datetime import date
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.dto_models import TicketPreisDTO


class TicketPreisService:
    def __init__(self, connection: Connection = Depends(get_db())):
        self._connection = connection


    def get_preis(
            self,
            fahrplan_nr: int, 
            wagon_nr: int, 
            abfahrt_bahnhof: str, 
            ankunft_bahnhof: str, 
            datum: date,
    ) -> TicketPreisDTO:
        with self._connection.cursor() as cursor:
            anz_stationen = None
            preis_je_haltestelle = None
            reservierungsaufschlag = None
            for row in cursor.execute(
                """
                    SELECT COUNT(*)
                    FROM STRECKENABSCHNITT S1
                    WHERE S1.FAHRPLAN_NR = :fp
                    AND S1.ABFAHRTSZEIT >= (
                        SELECT S2.ABFAHRTSZEIT
                        FROM STRECKENABSCHNITT S2
                        WHERE S2.FAHRPLAN_NR = S1.FAHRPLAN_NR
                        AND S2.ABFAHRT_BAHNHOF_NAME = :abhf
                    ) AND S1.ANKUNFTSZEIT <= (
                        SELECT S2.ANKUNFTSZEIT
                        FROM STRECKENABSCHNITT S2
                        WHERE S2.FAHRPLAN_NR = S1.FAHRPLAN_NR
                        AND S2.ANKUNFT_BAHNHOF_NAME = :akbhf
                    )
                """, [fahrplan_nr, abfahrt_bahnhof, ankunft_bahnhof]):
                anz_stationen = row[0]
            for row in cursor.execute(
                """
                    SELECT P.KOSTEN
                    FROM PREIS_JE_HALTESTELLE P
                    WHERE P.VON <= :datum
                    AND COALESCE(P.BIS, TO_DATE('31129999', 'ddmmyyyy')) > :datum
                """, [datum, datum]):
                preis_je_haltestelle = row[0]
            for row in cursor.execute(
                """
                    SELECT R.KOSTEN
                    FROM RESERVIERUNGSAUFSCHLAG R
                    INNER JOIN WAGON W
                    ON W.WAGONTYP_BEZEICHNUNG = R.WAGONTYP_BEZEICHNUNG
                    INNER JOIN FAHRPLAN FP
                    ON FP.ZUG_ZUGNUMMER = W.ZUG_ZUGNUMMER
                    WHERE R.VON <= :datum
                    AND COALESCE(R.BIS, TO_DATE('31129999', 'ddmmyyyy')) > :datum
                    AND W.REIHENFOLGE = :rf
                    AND FP.NR = :fpn
                """, [datum, datum, wagon_nr, fahrplan_nr]
            ):
                reservierungsaufschlag = row[0]

            return TicketPreisDTO(
                anzahl_stationen=anz_stationen, 
                preis_je_station=preis_je_haltestelle, 
                ticketpreis=preis_je_haltestelle*anz_stationen,
                reservierungsaufschlag=reservierungsaufschlag,
                gesamtkosten=preis_je_haltestelle*anz_stationen + reservierungsaufschlag)