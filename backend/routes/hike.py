import uuid
from database.schemas import HikeDetail, HikeListItem
from deps import SessionDep
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import selectinload
from database.models import Hike
from sqlalchemy import select

router = APIRouter(prefix="/hikes", tags=["hikes"])


@router.get("", response_model=list[HikeListItem])
def list_hikes(db: SessionDep, region: str | None = None):
    stmt = select(Hike)
    if region:
        stmt = stmt.where(Hike.region == region)
    return list(db.scalars(stmt))


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
