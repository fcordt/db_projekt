from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.python_sw.dto_models import WagonDTO, ZugDTO


class ZugService:
    def __init__(self, connection: Connection = Depends(get_db())):
        self._connection = connection

    def _get_wagons(self, fahrplan_nr: int, abfahrt_bahnhof: str, ankunft_bahnhof: str) -> list[WagonDTO]:
        r_val = []
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

            for wagon in cursor.execute("""
                                          SELECT 
                                            W.REIHENFOLGE,
                                            W.WAGONTYP_BEZEICHNUNG,
                                            W.KLASSE_ID,
                                            W.ZUG_ZUGNUMMER
                                          FROM WAGON W
                                          INNER JOIN FAHRPLAN FP
                                          ON W.ZUG_ZUGNUMMER = FP.ZUG_ZUGNUMMER
                                          WHERE FP.NR = :fpnr
                                          ORDER BY W.REIHENFOLGE ASC
                                          """, [fahrplan_nr]):
                freie_plaetze = []
                for platz in cursor.execute("""
                                                SELECT
                                                    S.SITZPLATZNUMMER
                                                FROM SITZPLATZ S
                                                WHERE S.WAGON_ZUGNUMMER = :znr
                                                AND S.WAGON_REIHENFOLGE = :rf
                                                AND NOT EXIST (
                                                    SELECT 1 FROM EINZELTICKET_MIT_SPR E
                                                    INNER JOIN EINZELTICKET ET
                                                    ON E.TICKETNUMMER = ET.TICKETNUMMER
                                                    WHERE COALESCE(E.RESERVIERDATUM, TO_DATE('01011991', 'ddmmyyyy')) > sysdate - interval '10' minute
                                                    AND ET.ABFAHRT_BAHNHOF_NAME IN (
                                                        :bfaf
                                                    )
                                                    AND ET.ANKUNFT_BAHNHOF_NAME IN (
                                                        :bfak
                                                    )
                                                )
                                            """, [wagon[3], wagon[0], ankunft_bahnhoefe, abfahrt_bahnhoefe]):
                    freie_plaetze.append(platz[0])
                r_val.append(WagonDTO(wagontyp=wagon[1], klasse=wagon[2], freie_sitze=freie_plaetze))
        return r_val
            

    def get_zug(self, fahrplan_nr: int, abfahrt_bahnhof: str, ankunft_bahnhof: str):
        wagons = self._get_wagons(fahrplan_nr, abfahrt_bahnhof, ankunft_bahnhof)
        with self._connection.cursor() as cursor:
            for zug in cursor.execute(  """
                                            SELECT Z.NAME, Z.ZUGNUMMER, T.NAME
                                            FROM ZUG Z
                                            INNER JOIN ZUGTYP T
                                            ON T.ID = Z.ZUGTYP_ID
                                            INNER JOIN FAHRPLAN FP
                                            ON FP.ZUG_ZUGNUMMER = Z.ZUGNUMMER
                                            WHERE FP.NR = :nummer
                                        """, [fahrplan_nr]):
                return ZugDTO(name=zug[0], zugnummer=zug[1], zugtyp=zug[2], wagen=wagons)

        