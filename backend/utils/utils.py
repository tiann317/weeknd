import requests
import xml.etree.ElementTree as ET
from backend.core.config import DB_API_KEY, DB_CLIENT_ID
from datetime import datetime, timedelta

STADA_URL = (
    "https://apis.deutschebahn.com/db-api-marketplace/apis/station-data/v2/stations"
)
TIMETABLES_URL = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1"

HEADERS = {
    "DB-Client-Id": DB_CLIENT_ID,
    "DB-Api-Key": DB_API_KEY,
    "Accept": "application/json",
}


def get_nearest_eva(lat: float, lon: float) -> dict | None:
    r = requests.get(STADA_URL, headers=HEADERS, timeout=30)
    r.raise_for_status()

    nearest, nearest_dist = None, float("inf")
    for station in r.json().get("result", []):
        try:
            coords = station["evaNumbers"][0]["geographicCoordinates"]["coordinates"]
            s_lat, s_lon = float(coords[1]), float(coords[0])
            eva = station["evaNumbers"][0]["number"]
            name = station["name"]
        except Exception:
            continue

        dist = (lat - s_lat) ** 2 + (lon - s_lon) ** 2
        if dist < nearest_dist:
            nearest_dist = dist
            nearest = {"name": name, "eva": eva, "lat": s_lat, "lon": s_lon}

    return nearest


def get_eva_by_name(name: str) -> dict | None:
    r = requests.get(
        STADA_URL, headers=HEADERS, params={"searchstring": name}, timeout=30
    )
    r.raise_for_status()
    results = r.json().get("result", [])
    if not results:
        return None
    return {
        "name": results[0]["name"],
        "eva": results[0]["evaNumbers"][0]["number"],
    }


def get_connection(from_eva: str, to_name: str, dt: datetime) -> dict | None:
    date = dt.strftime("%y%m%d")
    hour = dt.strftime("%H")

    r = requests.get(
        f"{TIMETABLES_URL}/plan/{from_eva}/{date}/{hour}", headers=HEADERS, timeout=30
    )
    if r.status_code != 200:
        return None

    root = ET.fromstring(r.text)
    candidates = []
    for s in root.findall("s"):
        dp, tl = s.find("dp"), s.find("tl")
        if dp is None or tl is None:
            continue
        if to_name not in dp.attrib.get("ppth", ""):
            continue
        candidates.append(
            {
                "trip_id": s.attrib.get("id"),
                "type": tl.attrib.get("c"),
                "number": tl.attrib.get("n"),
                "line": dp.attrib.get("l")
                or f"{tl.attrib.get('c')} {tl.attrib.get('n')}",
                "departure": dp.attrib.get("pt"),
            }
        )

    if not candidates:
        return None

    train = candidates[0]
    dep_dt = datetime.strptime(train["departure"], "%y%m%d%H%M")

    to_station = get_eva_by_name(to_name)
    if not to_station:
        return None

    arrival = None
    for h_offset in range(4):
        check_dt = dep_dt + timedelta(hours=h_offset)
        r2 = requests.get(
            f"{TIMETABLES_URL}/plan/{to_station['eva']}/{date}/{check_dt.strftime('%H')}",
            headers=HEADERS,
            timeout=30,
        )
        if r2.status_code != 200:
            continue
        for s in ET.fromstring(r2.text).findall("s"):
            tl2 = s.find("tl")
            ar2 = s.find("ar")
            if tl2 is None or ar2 is None:
                continue
            if tl2.attrib.get("n") != train["number"]:
                continue
            arr_time = ar2.attrib.get("pt")
            if not arr_time:
                continue
            arr_dt = datetime.strptime(arr_time, "%y%m%d%H%M")
            if arr_dt > dep_dt:
                arrival = arr_time
                break
        if arrival:
            break

    label = train["line"]
    return {
        "line": label,
        "departure": db_time_to_str(train["departure"]) if train["departure"] else None,
        "arrival": db_time_to_str(arrival) if arrival else None,
    }


def fetch_departures(eva_id: str) -> list:
    now = datetime.now()
    r = requests.get(
        f"{TIMETABLES_URL}/plan/{eva_id}/{now.strftime('%y%m%d')}/{now.strftime('%H')}",
        headers=HEADERS,
        timeout=30,
    )
    if r.status_code != 200:
        return []

    trains = []
    for s in ET.fromstring(r.text).findall("s"):
        tl, dp, ar = s.find("tl"), s.find("dp"), s.find("ar")
        if tl is None or dp is None:
            continue
        trains.append(
            {
                "type": tl.attrib.get("c"),
                "number": tl.attrib.get("n"),
                "line": dp.attrib.get("l")
                or (ar.attrib.get("l") if ar is not None else None),
                "trip_id": s.attrib.get("id"),
                "departure": dp.attrib.get("pt"),
                "arrival": ar.attrib.get("pt") if ar is not None else None,
                "dp_ppth": dp.attrib.get("ppth"),
                "ar_ppth": ar.attrib.get("ppth") if ar is not None else None,
            }
        )
    return trains


def fetch_trip_stops(train: dict, station_name: str) -> list:
    stops = []
    if train.get("ar_ppth"):
        for name in train["ar_ppth"].split("|"):
            stops.append({"station": name, "arrival": None, "departure": None})
    stops.append(
        {
            "station": station_name,
            "arrival": train.get("arrival"),
            "departure": train.get("departure"),
        }
    )
    if train.get("dp_ppth"):
        for name in train["dp_ppth"].split("|"):
            stops.append({"station": name, "arrival": None, "departure": None})
    return stops


def db_time_to_str(db_time: str) -> str:
    return datetime.strptime(db_time, "%y%m%d%H%M").strftime("%Y-%m-%d %H:%M")


def to_db_time(db_time: str) -> str:
    return datetime.strptime(db_time, "%Y-%m-%d %H:%M").strftime("%y%m%d%H%M")


def print_stops(train_label: str, stops: list):
    print(f"\n=== Stops for {train_label} ===\n")
    for i, stop in enumerate(stops):

        def fmt(t):
            if not t:
                return "-"
            return datetime.strptime(t, "%y%m%d%H%M").strftime("%H:%M")

        print(
            f"{i:02d} {stop['station'] or 'Unknown':<30} "
            f"Arr: {fmt(stop['arrival'])}  Dep: {fmt(stop['departure'])}"
        )


def print_trains(station_name: str, trains: list):
    print(f"\n=== Departures: {station_name} ===\n")
    if not trains:
        print("No trains found")
        return
    for train in trains[:20]:
        print(
            f"{train['type']} {train['number']:<10} "
            f"Departure: {train['departure']}  Arrival: {train['arrival']}"
        )
