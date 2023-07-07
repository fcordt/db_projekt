from typing import List
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.dto_models import TrainStationDTO


class BahnhofService:
    def __init__(self, connection: Connection = Depends(get_db())):
        self._connection = connection

    def get_stations(self, name="") -> List[TrainStationDTO]:
        with self._connection.cursor() as cursor:
            return list(
                map(
                    lambda x: TrainStationDTO(
                        name=x[0], adresse=x[1], plz=x[2], ort=x[3], bahnsteige=x[4]
                    ),
                    cursor.execute(
                        """
            SELECT B.NAME, B.ADRESSE, O.PLZ, O.NAME, COUNT(BS.NR)
            FROM BAHNHOF B
            INNER JOIN ORT O
            ON B.ORT_PLZ = O.PLZ 
            INNER JOIN BAHNSTEIG BS
            ON BS.BAHNHOF_NAME  = B.NAME 
            WHERE B.NAME LIKE :customName
            GROUP BY B.NAME, B.ADRESSE, O.PLZ, O.NAME
            """,
                        customName=f"%{name}%",
                    ),
                )
            )
