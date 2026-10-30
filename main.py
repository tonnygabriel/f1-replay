from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import pandas as pd

fastf1.Cache.enable_cache('cache')

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


def load_session(year: int, gp: str, session_type: str):
    session = fastf1.get_session(year, gp, session_type)
    session.load()
    return session


def driver_telemetry(session, drv_number: str):
    laps = session.laps.pick_drivers(drv_number)
    if laps.empty:
        return None
    car = laps.get_car_data()
    pos = laps.get_pos_data()
    merged = pd.merge_asof(
        pos.sort_values('SessionTime'),
        car[['SessionTime', 'Brake', 'Speed']].sort_values('SessionTime'),
        on='SessionTime', direction='nearest'
    )
    merged['t'] = merged['SessionTime'].dt.total_seconds()
    return merged[['t', 'X', 'Y', 'Brake', 'Speed']].to_dict(orient='records')


@app.get("/calendar/{year}")
def calendar(year: int):
    try:
        schedule = fastf1.get_event_schedule(year)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return schedule[['RoundNumber', 'EventName', 'Location']].to_dict(orient='records')


@app.get("/session/{year}/{gp}/{session_type}")
def full_session(year: int, gp: str, session_type: str):
    try:
        session = load_session(year, gp, session_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = {}
    for drv in session.drivers:
        telemetry = driver_telemetry(session, drv)
        if telemetry is None:
            continue
        code = session.get_driver(drv)['Abbreviation']
        result[code] = telemetry

    if not result:
        raise HTTPException(status_code=404, detail="no telemetry found for this session")
    return result


@app.get("/session/{year}/{gp}/{session_type}/{driver}")
def single_driver(year: int, gp: str, session_type: str, driver: str):
    try:
        session = load_session(year, gp, session_type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    telemetry = driver_telemetry(session, driver)
    if telemetry is None:
        raise HTTPException(status_code=404, detail=f"no laps found for driver {driver}")
    return telemetry