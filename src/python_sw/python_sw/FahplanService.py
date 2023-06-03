from datetime import datetime
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db_service
from python_sw.dto_models import BahnsteigFahrtDTO, FahplanStopDTO, FahrplanDTO


class FahrplanService:
    def __init__(self, connection: Connection = Depends(get_db_service)):
        self._connection = connection

    def get_fahrplaene(
        self, von: datetime = datetime(1991, 1, 1), bis: datetime = datetime(9999, 1, 1)
    ):
        with self._connection.cursor() as cursor:
            return list(
                map(
                    lambda x: FahrplanDTO(nr=x[0], name=x[1], von=x[2], bis=x[3]),
                    cursor.execute(
                        "SELECT NR, Name, VON_DATUM, BIS_DATUM FROM FAHRPLAN WHERE VON_DATUM < :bis_date AND BIS_DATUM > :von_date",
                        von_date=von,
                        bis_date=bis,
                    ),
                )
            )

    def get_fahrplan_details(self, fahrplan_nr: int):
        with self._connection.cursor() as cursor:
            rs = cursor.execute(
                """
                SELECT 
                S.ABFAHRTSZEIT , S.ANKUNFTSZEIT, 
                S.ABFAHRT_BAHNSTEIG_NR , S.ANKUNFT_BAHNSTEIG_NR , 
                S.ABFAHRT_BAHNHOF_NAME , S.ANKUNFT_BAHNHOF_NAME  
                FROM DBUSER.STRECKENABSCHNITT S
                WHERE FAHRPLAN_NR = :fpnr
                ORDER BY ABFAHRTSZEIT ASC
            """,
                fpnr=fahrplan_nr,
            )
            rv = []
            for item in rs:
                start = None
                end = None
                if item[0]:
                    start = BahnsteigFahrtDTO(
                        uhrzeit=item[0], bahnsteig_nr=item[2], bahnhof_name=item[4]
                    )
                if item[1]:
                    end = BahnsteigFahrtDTO(
                        uhrzeit=item[1], bahnsteig_nr=item[3], bahnhof_name=item[5]
                    )
                rv.append(FahplanStopDTO(abfahrt=start, ankunft=end))
            return rv
