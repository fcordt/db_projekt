from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.python_sw.dto_models import WagonDTO, ZugDTO


class ZugService:
    def __init__(self, connection: Connection = Depends(get_db())):
        self._connection = connection

    def _get_wagons(self, zugnummer: int) -> list[WagonDTO]:
        r_val = []
        with self._connection.cursor() as cursor:
            for wagon in cursor.execute("""
                                          SELECT 
                                            W.REIHENFOLGE,
                                            W.WAGONTYP_BEZEICHNUNG,
                                            W.KLASSE_ID
                                          FROM WAGON W
                                          WHERE W.ZUG_ZUGNUMMER = :zug
                                          ORDER BY W.REIHENFOLGE ASC
                                          """, [zugnummer]):
                freie_plaetze = []
                for platz in cursor.execute("""
                                                SELECT
                                                    S.SITZPLATZNUMMER
                                                FROM SITZPLATZ S
                                                WHERE S.WAGON_ZUGNUMMER = :znr
                                                AND S.WAGON_REIHENFOLGE = :rf
                                                AND NOT EXIST (
                                                    SELECT 1 FROM EINZELTICKET_MIT_SPR E
                                                    WHERE COALESCE(E.RESERVIERDATUM, TO_DATE('01011991', 'ddmmyyyy')) > sysdate - interval '10' minute
                                                )
                                            """, [zugnummer, wagon[0]]):
                    freie_plaetze.append(platz[0])
                r_val.append(WagonDTO(wagontyp=wagon[1], klasse=wagon[2], freie_sitze=freie_plaetze))
        return r_val
            

    def get_zug(self, zugnummer: int):
        wagons = self._get_wagons(zugnummer)
        with self._connection.cursor() as cursor:
            for zug in cursor.execute(  """
                                            SELECT Z.NAME, T.NAME
                                            FROM ZUG Z
                                            INNER JOIN ZUGTYP T
                                            ON T.ID = Z.ZUGTYP_ID
                                            WHERE Z.ZUGNUMMER = :nummer
                                        """, [zugnummer]):
                return ZugDTO(name=zug[0], zugnummer=zugnummer, zugtyp=zug[2], wagen=wagons)

        