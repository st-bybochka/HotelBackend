from fastapi import APIRouter, Depends
from datetime import date

from app.booking.dao import BookingDao
from app.booking.schemas import ShemBooking
from app.exceptions import RoomCannotBookedError
from app.user.models.user_model import Users
from app.user.dependencies import current_user

router = APIRouter(
    prefix="/booking",
    tags=["Бронирования"],
)

@router.get("/my_bookings")
async def get_my_bookings(user: Users = Depends(current_user)) -> list[ShemBooking]:
    return await BookingDao.get_all(user_id=user.id)


@router.post("/")
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(current_user),

):
    booking = await BookingDao.add_booking(user_id=user.id, room_id=room_id, date_from=date_from, date_to=date_to)
    if not booking:
        raise RoomCannotBookedError


@router.post("/delete_booking")
async def delete_booking(
        booking_id: int,
        user: Users = Depends(current_user)):
    await BookingDao.delete_booking(user_id=user.id, booking_id=booking_id)