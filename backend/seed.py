from sqlalchemy import func, select

from core.db import SessionLocal
from database.models import Hike, SportType, Station


def run():
    with SessionLocal() as db:
        if db.scalar(select(func.count(Hike.id))) > 0:
            print("already seeded")
            return

        # --- stations (D-Ticket reference / deny-list lives here) ---
        garmisch = Station(
            name="Garmisch-Partenkirchen", lat=47.491, lon=11.095,
            operator="DB Regio", is_private_railway=False, dticket_valid=True,
        )
        zugspitze = Station(
            name="Zugspitzplatt (BZB)", lat=47.418, lon=10.980,
            operator="Bayerische Zugspitzbahn", is_private_railway=True, dticket_valid=False,
        )
        kochel = Station(
            name="Kochel", lat=47.660, lon=11.357,
            operator="DB Regio", is_private_railway=False, dticket_valid=True,
        )
        herrsching = Station(
            name="Herrsching", lat=48.001, lon=11.176,
            operator="DB Regio (S8)", is_private_railway=False, dticket_valid=True,
        )
        db.add_all([garmisch, zugspitze, kochel, herrsching])
        db.flush()

        # --- hikes (coords approximate, verify on curation) ---
        db.add_all([
            Hike(
                title="Partnachklamm", region="Garmisch", sport=SportType.hike,
                distance_km=7.0, duration_min=150, ascent_m=180, difficulty="easy",
                start_lat=47.492, start_lon=11.106, is_loop=True,
                start_station_id=garmisch.id,
            ),
            Hike(
                title="Eibsee-Runde", region="Garmisch", sport=SportType.hike,
                distance_km=7.5, duration_min=140, ascent_m=120, difficulty="easy",
                start_lat=47.457, start_lon=10.978, is_loop=True,
                start_station_id=garmisch.id,
            ),
            Hike(
                title="Kochelsee – Walchensee", region="Kochel", sport=SportType.hike,
                distance_km=11.0, duration_min=240, ascent_m=450, difficulty="moderate",
                start_lat=47.660, start_lon=11.357, is_loop=False,
                start_station_id=kochel.id,
            ),
            Hike(
                title="Herrsching → Kloster Andechs", region="Ammersee", sport=SportType.hike,
                distance_km=6.5, duration_min=120, ascent_m=200, difficulty="easy",
                start_lat=48.001, start_lon=11.176,
                end_lat=48.000, end_lon=11.187, is_loop=False,
                start_station_id=herrsching.id,
            ),
            # ⚠️ private-railway case: BZB is NOT D-Ticket valid
            Hike(
                title="Zugspitze Gipfel via Bayerische Zugspitzbahn", region="Garmisch",
                sport=SportType.hike,
                distance_km=4.0, duration_min=90, ascent_m=350, difficulty="hard",
                start_lat=47.418, start_lon=10.980, is_loop=False,
                start_station_id=zugspitze.id,
            ),
        ])
        db.commit()
        print("seeded")


if __name__ == "__main__":
    run()