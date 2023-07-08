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

    def get_free_tickets(self, fahrplan_nr: int, abfahrt_bahnhof: str, ankunft_bahnhof: str, datum: date, wagon_nr: int) -> list[int]:
        freie_plaetze = []
        with self._connection.cursor() as cursor:
            abfahrt_bahnhoefe = []
            ankunft_bahnhoefe = []

            for bahnhof in cursor.execute(  """
                                                SELECT SA.ANKUNFT_BAHNHOF_NAME
                                                FROM STRECKENABSCHNITT SA
                                                WHERE SA.FAHRPLANNR = :fp
                                                AND SA.ANKUNFTZEIT < (
                                                    SELECT SA1.ANKUNFTZEIT
                                                    FROM STRECKENABSCHNITT SA1
                                                    WHERE SA1.FAHRPLANNR = :fp
                                                    AND SA1.ANKUNFT_BAHNHOF = :bf
                                                )
                                            """, fp=fahrplan_nr, bf=ankunft_bahnhof):
                ankunft_bahnhoefe.append(bahnhof[0])
            for bahnhof in cursor.execute(  """
                                                SELECT SA.ABFAHRT_BAHNHOF_NAME
                                                FROM STRECKENABSCHNITT SA
                                                WHERE SA.FAHRPLANNR = :fp
                                                AND SA.ABFAHRTZEIT > (
                                                    SELECT SA1.ABFAHRTZEIT
                                                    FROM STRECKENABSCHNITT SA1
                                                    WHERE SA1.FAHRPLANNR = :fp
                                                    AND SA1.ABFAHRT_BAHNHOF = :bf
                                                )
                                            """, fp=fahrplan_nr, bf=abfahrt_bahnhof):
                abfahrt_bahnhoefe.append(bahnhof[0])
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
                                            AND NOT EXIST (
                                                SELECT 1 FROM EINZELTICKET_MIT_SPR E
                                                INNER JOIN EINZELTICKET ET
                                                ON E.TICKETNUMMER = ET.TICKETNUMMER
                                                INNER JOIN TICKET T
                                                ON E.TICKETNUMMER = T.TICKETNUMMER
                                                WHERE COALESCE(E.RESERVIERDATUM, TO_DATE('01011991', 'ddmmyyyy')) > sysdate - interval '10' minute
                                                AND ET.ABFAHRT_BAHNHOF_NAME IN (
                                                    :bfaf
                                                )
                                                AND ET.ANKUNFT_BAHNHOF_NAME IN (
                                                    :bfak
                                                )
                                                AND T.GÜLTIGKEITSDATUM = :dat
                                            )
                                        """, [wagon_nr, fahrplan_nr, ankunft_bahnhoefe, abfahrt_bahnhoefe, datum]):
                    freie_plaetze.append(platz[0])
        return freie_plaetze