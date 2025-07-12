from fastapi import APIRouter

from app.hotel.schemas import ShemHotelInfo, HotelsModel
from app.hotel.dao import HotelService

router = APIRouter(
    prefix="/hotel",
    tags=["Отель"]

)


@router.get("/get_hotels")
async def get_hotels() -> list[HotelsModel]:
    return await HotelService.get_hotels_by_stars()


@router.get("/get_hotels_by_location")
async def get_hotels_by_locations_and_date(
        location: str
):
    return await HotelService.get_available_rooms(location=location)
