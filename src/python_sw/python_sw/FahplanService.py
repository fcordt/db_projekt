from datetime import datetime
from typing import Optional
from fastapi import Depends
from oracledb import Connection

from python_sw.DbService import get_db
from python_sw.dto_models import BahnsteigFahrtDTO, BahnsteigFahrtInsertDTO, FahplanStopDTO, FahrplanDTO


class FahrplanService:
    def __init__(self, connection: Connection = Depends(get_db())):
        self._connection = connection

    def get_fahrplaene(
        self, abfahrt_bahnhof: str = None, ankunft_bahnhof: str = None, von: datetime = datetime(1991, 1, 1), bis: datetime = datetime(9999, 1, 1)
    ):
        bvars = []
        query = "SELECT FP.NR, FP.NAME, FP.VON_DATUM, FP.BIS_DATUM, FP.ZUG_ZUGNUMMER FROM DBUSER.FAHRPLAN FP"
        if abfahrt_bahnhof is not None:
            query += " INNER JOIN DBUSER.STRECKENABSCHNITT VSA ON VSA.FAHRPLAN_NR = FP.FAHRPLAN_NR AND VSA.ABFAHRT_BAHNHOF_NAME = :abfbhf"
            bvars.append(abfahrt_bahnhof)
        if ankunft_bahnhof is not None:
            query += " INNER JOIN DBUSER.STRECKENABSCHNITT BSA ON BSA.FAHRPLAN_NR = FP.FAHRPLAN_NR AND BSA.ANKUNFT_BAHNHOF_NAME = :ankbhf"
            bvars.append(ankunft_bahnhof)

        query += " WHERE VON_DATUM < :bis_date AND BIS_DATUM > :von_date"
        bvars.append(bis)
        bvars.append(von)
        if ankunft_bahnhof is not None and abfahrt_bahnhof is not None:
            query += " AND VSA.abfahrtszeit <= BFA.ankunftszeit"

        with self._connection.cursor() as cursor:
            return list(
                map(
                    lambda x: FahrplanDTO(nr=x[0], name=x[1], von=x[2], bis=x[3], zugnummer=x[4]),
                    cursor.execute(
                        query,
                        bvars
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
                S.ABFAHRT_BAHNHOF_NAME , S.ANKUNFT_BAHNHOF_NAME , S.ID  
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
                rv.append(FahplanStopDTO(abfahrt=start, ankunft=end, id=item[6]))
            return rv
        
    def delete_fahrplan_detail(self, detail_nr: int):
        with self._connection.cursor() as cursor:
            cursor.execute("""
                DELETE
                FROM DBUSER.STRECKENABSCHNITT S
                WHERE S.ID = :id
            """, id=detail_nr)

    def insert_fahrplan_detail(self, fahrplan_nr : int, abfahrt_bahnsteig: Optional[BahnsteigFahrtInsertDTO], ankunft_bahnsteig: Optional[BahnsteigFahrtInsertDTO]):
        with self._connection.cursor() as cursor:
            cursor.execute("""
                INSERT
                INTO DBUSER.STRECKENABSCHNITT(abfahrtszeit, ankunftszeit, fahrplan_nr, abfahrt_bahnsteig_nr, ankunft_bahnsteig_nr, abfahrt_bahnhof_name, ankunft_bahnhof_name)
                VALUES (:abfahrtszeit, :ankunftszeit, :fahrplan_nr, :abfahrt_bahnsteig_nr, :ankunft_bahnsteig_nr, :abfahrt_bahnhof_name, :ankunft_bahnhof_name)
            """, 
            abfahrtszeit=abfahrt_bahnsteig.uhrzeit if abfahrt_bahnsteig is not None else None,    
            ankunftszeit=ankunft_bahnsteig.uhrzeit if abfahrt_bahnsteig is not None else None,           
            fahrplan_nr=fahrplan_nr,         
            abfahrt_bahnsteig_nr=abfahrt_bahnsteig.bahnsteig_nr if abfahrt_bahnsteig is not None else None,   
            ankunft_bahnsteig_nr=ankunft_bahnsteig.bahnsteig_nr if abfahrt_bahnsteig is not None else None,   
            abfahrt_bahnhof_name=abfahrt_bahnsteig.bahnhof_name if abfahrt_bahnsteig is not None else None,   
            ankunft_bahnhof_name=ankunft_bahnsteig.bahnhof_name if abfahrt_bahnsteig is not None else None)

    def update_fahrplan_detail(self, detail_nr : int, abfahrt_bahnsteig: Optional[BahnsteigFahrtInsertDTO], ankunft_bahnsteig: Optional[BahnsteigFahrtInsertDTO]):
        with self._connection.cursor() as cursor:
            cursor.execute("""
                UPDATE DBUSER.STRECKENABSCHNITT
                SET 
                    abfahrtszeit=:abfahrtszeit, 
                    ankunftszeit=:ankunftszeit,
                    abfahrt_bahnsteig_nr=:abfahrt_bahnsteig_nr,
                    ankunft_bahnsteig_nr=:ankunft_bahnsteig_nr,
                    abfahrt_bahnhof_name=:abfahrt_bahnhof_name,
                    ankunft_bahnhof_name=:ankunft_bahnhof_name
                WHERE id = :detail_nr
                """, 
            abfahrtszeit=abfahrt_bahnsteig.uhrzeit if abfahrt_bahnsteig is not None else None,    
            ankunftszeit=ankunft_bahnsteig.uhrzeit if abfahrt_bahnsteig is not None else None,           
            detail_nr=detail_nr,         
            abfahrt_bahnsteig_nr=abfahrt_bahnsteig.bahnsteig_nr if abfahrt_bahnsteig is not None else None,   
            ankunft_bahnsteig_nr=ankunft_bahnsteig.bahnsteig_nr if abfahrt_bahnsteig is not None else None,   
            abfahrt_bahnhof_name=abfahrt_bahnsteig.bahnhof_name if abfahrt_bahnsteig is not None else None,   
            ankunft_bahnhof_name=ankunft_bahnsteig.bahnhof_name if abfahrt_bahnsteig is not None else None)
