from datetime import date
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db


class FreePlaceService:
    def __init__(self, connection: Connection):
        self._connection = connection

    def is_ticket_free(self, ticket_nr: int):
        with self._connection.cursor() as cursor:
            for row in cursor.execute("SELECT COUNT(*) FROM EINZELTICKET_MIT_SPR WHERE E.TICKETNUMMER = :tnr AND COALESCE(E.RESERVIERDATUM, TO_DATE('01011991', 'ddmmyyyy')) > sysdate - interval '10' minute",
                                      [ticket_nr]):
                return row[0] == 0

    def get_free_seats(self, fahrplan_nr: int, abfahrt_bahnhof: str, ankunft_bahnhof: str, datum: date, wagon_nr: int) -> list[int]:
        freie_plaetze = []
        with self._connection.cursor() as cursor:
            for platz in cursor.execute("""
                                            SELECT
                                                S.SITZPLATZNUMMER
                                            FROM SITZPLATZ S
                                            INNER JOIN WAGON W
                                            ON W.ZUG_ZUGNUMMER = S.WAGON_ZUGNUMMER
                                            AND W.REIHENFOLGE = S.WAGON_REIHENFOLGE
                                            INNER JOIN FAHRPLAN P
                                            ON P.ZUG_ZUGNUMMER = W.ZUG_ZUGNUMMER
                                            WHERE S.WAGON_REIHENFOLGE = :rf
                                            AND P.NR = :fpnr
                                            AND NOT EXISTS (
                                                SELECT 1 FROM EINZELTICKET_MIT_SPR E
                                                INNER JOIN EINZELTICKET ET
                                                ON E.TICKETNUMMER = ET.TICKETNUMMER
                                                INNER JOIN TICKET T
                                                ON E.TICKETNUMMER = T.TICKETNUMMER
                                                WHERE COALESCE(E.RESERVIERDATUM, TO_DATE('01011991', 'ddmmyyyy')) > (sysdate - interval '10' minute)
                                                AND ET.ABFAHRT_BAHNHOF_NAME IN (
                                                    SELECT SA.ANKUNFT_BAHNHOF_NAME
                                                    FROM STRECKENABSCHNITT SA
                                                    WHERE SA.FAHRPLAN_NR = :fpnr
                                                    AND SA.ANKUNFTSZEIT < (
                                                        SELECT SA1.ANKUNFTSZEIT
                                                        FROM STRECKENABSCHNITT SA1
                                                        WHERE SA1.FAHRPLAN_NR = :fpnr
                                                        AND SA1.ANKUNFT_BAHNHOF_NAME = :ankunft_bahnhof
                                                    )
                                                )
                                                AND ET.ANKUNFT_BAHNHOF_NAME IN (
                                                    SELECT SA.ABFAHRT_BAHNHOF_NAME
                                                    FROM STRECKENABSCHNITT SA
                                                    WHERE SA.FAHRPLAN_NR = :fpnr
                                                    AND SA.ABFAHRTSZEIT > (
                                                        SELECT SA1.ABFAHRTSZEIT
                                                        FROM STRECKENABSCHNITT SA1
                                                        WHERE SA1.FAHRPLAN_NR = :fpnr
                                                        AND SA1.ABFAHRT_BAHNHOF_NAME = :abfahrt_bahnhof
                                                    )
                                                )
                                                AND T.GÜLTIGKEITSDATUM = :dat
                                            )
                                        """, rf=wagon_nr, fpnr=fahrplan_nr, ankunft_bahnhof=ankunft_bahnhof, abfahrt_bahnhof=abfahrt_bahnhof, dat=datum):
                    freie_plaetze.append(platz[0])
        return freie_plaetze