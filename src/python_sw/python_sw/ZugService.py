from datetime import date
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.FreePlaceService import FreePlaceService
from python_sw.dto_models import WagonDTO, ZugDTO


class ZugService:
    def __init__(self, connection: Connection = Depends(get_db())):
        self._connection = connection

    def _get_wagons(self, fahrplan_nr: int, abfahrt_bahnhof: str, ankunft_bahnhof: str, datum: date) -> list[WagonDTO]:
        r_val = []
        with self._connection.cursor() as cursor:
            for wagon in cursor.execute("""
                                          SELECT 
                                            W.REIHENFOLGE,
                                            W.WAGONTYP_BEZEICHNUNG,
                                            W.KLASSE_ID
                                          FROM WAGON W
                                          INNER JOIN FAHRPLAN FP
                                          ON W.ZUG_ZUGNUMMER = FP.ZUG_ZUGNUMMER
                                          WHERE FP.NR = :fpnr
                                          ORDER BY W.REIHENFOLGE ASC
                                          """, [fahrplan_nr]):
                freie_plaetze = FreePlaceService(
                        connection=self._connection
                    ).get_free_seats(
                        fahrplan_nr=fahrplan_nr, 
                        abfahrt_bahnhof=abfahrt_bahnhof, 
                        ankunft_bahnhof=ankunft_bahnhof, 
                        datum=datum,
                        wagon_nr=wagon[0])
                r_val.append(WagonDTO(
                    wagonnummer=wagon[0],
                    wagontyp=wagon[1], 
                    klasse=wagon[2], 
                    freie_sitze=freie_plaetze))
        return r_val
            

    def get_zug(self, fahrplan_nr: int, abfahrt_bahnhof: str, ankunft_bahnhof: str, date: date):
        wagons = self._get_wagons(fahrplan_nr, abfahrt_bahnhof, ankunft_bahnhof, date)
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

        