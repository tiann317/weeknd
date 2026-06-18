import uuid
from database.schemas import HikeDetail, HikeListItem
from deps import SessionDep
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from database.models import Hike
from sqlalchemy import select, text

router = APIRouter(prefix="/hikes", tags=["hikes"])


@router.get("", response_model=list[HikeListItem])
def list_hikes(db: SessionDep, region: str | None = None):
    stmt = select(Hike)
    if region:
        stmt = stmt.where(Hike.region == region)
    return list(db.scalars(stmt))


@router.get("/nearby", response_model=list[HikeListItem])
def nearby_hikes(db: SessionDep, lat: float, lon: float, radius_km: float = 30):
    radius_m = radius_km * 1000
    stmt = text("""
          SELECT *
          FROM hikes
          WHERE earth_box(ll_to_earth(:lat, :lon), :radius_m)
                @> ll_to_earth(start_lat, start_lon)
            AND earth_distance(ll_to_earth(:lat, :lon),
                               ll_to_earth(start_lat, start_lon)) <=
  :radius_m
          ORDER BY earth_distance(ll_to_earth(:lat, :lon),
                                 ll_to_earth(start_lat, start_lon)) ASC
      """)
    rows = db.execute(stmt, {"lat": lat, "lon": lon, "radius_m": radius_m})
    return rows.mappings().all()


@router.get("/{hike_id}", response_model=HikeDetail)
def get_hike(hike_id: uuid.UUID, db: SessionDep):
    hike = db.scalar(
        select(Hike)
        .where(Hike.id == hike_id)
        .options(selectinload(Hike.start_station), selectinload(Hike.end_station))
    )
    if not hike:
        raise HTTPException(404, "Hike not found")
    return hike
