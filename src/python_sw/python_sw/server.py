from typing import Optional
from fastapi import Body, Depends, FastAPI, Path, Query
from python_sw.UserService import UserService

from python_sw.BahnhofService import BahnhofService
from python_sw.FahplanService import FahrplanService
from python_sw.dto_models import BahnsteigFahrtDTO, BahnsteigFahrtInsertDTO, FahplanStopDTO, FahrplanDTO, TrainStationDTO, UserDTO

app = FastAPI()


@app.get("/api/v1/stations", response_model=list[TrainStationDTO])
def get_bahnhof(name: Optional[str] = "", bahnhof_service: BahnhofService = Depends()):
    return bahnhof_service.get_stations(name)

@app.get("/api/v1/schedules", response_model=list[FahrplanDTO])
def get_fahrplan(
        abfahrt_bahnhof: Optional[str] = Query(default=None),
        ankunft_bahnhof: Optional[str] = Query(default=None),
        fahrplan_service: FahrplanService = Depends()
    ):
    return fahrplan_service.get_fahrplaene(abfahrt_bahnhof, ankunft_bahnhof)


@app.get("/api/v1/schedules/{nr}", response_model=list[FahplanStopDTO])
def get_fahrplan(nr: int, fahrplan_service: FahrplanService = Depends()):
    return fahrplan_service.get_fahrplan_details(nr)

@app.delete("/api/v1/schedule-details/{id}", status_code=200)
def delete_schedule(id: int, fahrplan_service: FahrplanService = Depends()):
    fahrplan_service.delete_fahrplan_detail(nr)

@app.post("/api/v1/schedule-details", status_code=201)
def post_schedult_details(
        fahrplan_nr: int = Body(),
        abfahrt_bahnsteig: Optional[BahnsteigFahrtInsertDTO] = Body(default=None),
        ankunft_bahnsteig: Optional[BahnsteigFahrtInsertDTO] = Body(default=None),
        fahrplan_service: FahrplanService = Depends()
    ):
        assert abfahrt_bahnsteig is not None or ankunft_bahnsteig is not None
        fahrplan_service.insert_fahrplan_detail(fahrplan_nr, abfahrt_bahnsteig, ankunft_bahnsteig)

@app.put("/api/v1/schedule-details/{id}", status_code=200)
def put_schedult_details(
        id: int,
        abfahrt_bahnsteig: Optional[BahnsteigFahrtInsertDTO] = Body(default=None),
        ankunft_bahnsteig: Optional[BahnsteigFahrtInsertDTO] = Body(default=None),
        fahrplan_service: FahrplanService = Depends()
    ):
        assert abfahrt_bahnsteig is not None or ankunft_bahnsteig is not None
        fahrplan_service.update_fahrplan_detail(id, abfahrt_bahnsteig, ankunft_bahnsteig)

@app.get("/api/v1/users", response_model=list[UserDTO])
def get_users(
        vorname: Optional[str] = Query(default=None),
        nachname:  Optional[str] = Query(default=None),
        adresse:  Optional[str] = Query(default=None),
        plz:  Optional[str] = Query(default=None),
        ort:  Optional[str] = Query(default=None),
        user_Service: UserService = Depends()
    ):
    return user_Service.get_users(vorname, nachname, adresse, plz, ort)

@app.get("/api/v1/users/{nr}", response_model=UserDTO)
def get_user(nr: str = Path(), user_service: UserService = Depends()):
    return user_service.get_user_by_kundennummer(nr)

@app.post("/api/v1/users", status_code=201)
def post_user(kundennummer: str = Body(), 
              vorname: str = Body(),
              nachname: str = Body(),
              adresse: str = Body(),
              plz: str= Body(),
             user_service: UserService = Depends()):
    user_service.insert_kunde(kundennummer=kundennummer, vorname=vorname, nachname=nachname, adresse=adresse, plz=plz)

@app.put("/api/v1/users/{nr}", status_code=200)
def put_user(nr: str = Path(), 
              vorname: str = Body(),
              nachname: str = Body(),
              adresse: str = Body(),
              plz: str= Body(),
             user_service: UserService = Depends()):
    user_service.update_kunde(kundennummer=nr, vorname=vorname, nachname=nachname, adresse=adresse, plz=plz)

@app.delete("/api/v1/users/{nr}", status_code=200)
def post_user(nr: str = Path(), 
             user_service: UserService = Depends()):
    user_service.delete_kunde(kundennummer=nr)