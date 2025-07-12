from dns.e164 import query
from pydantic.v1.errors import cls_kwargs
from sqlalchemy import select, insert, func, and_, or_, delete
from datetime import date

from app.dao.base_dao import BaseDao
from app.database import async_session_maker
from app.room.rooms_model import Rooms
from app.booking.bookings_model import Bookings


class BookingDao(BaseDao):
    model = Bookings

    @classmethod
    async def delete_booking(cls, user_id: int, booking_id: int):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(user_id=user_id, id=booking_id)
            await session.execute(query)
            await session.commit()


    @classmethod
    async def add_booking(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """WITH booked_rooms AS (
	        SELECT * FROM bookings
	        WHERE room_id = 1 AND
	        (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
	        (date_from <= '2023-05-15' AND date_to > '2023-05-15')
	        )
        SELECT (rooms.quantity - COUNT(booked_rooms.room_id)) AS count_rooms FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms.room_id"""



        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")

            rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("count_rooms")
            ).select_from(Rooms).outerjoin(
                booked_rooms, booked_rooms.c.room_id == Rooms.id
            ).where(
                Rooms.id == room_id
            ).group_by(
                Rooms.quantity,
                booked_rooms.c.room_id
            )

            result = await session.execute(rooms_left)
            rooms_left1: int = result.scalar()

            if rooms_left1 > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price1 = await session.execute(get_price)
                price: int = price1.scalar()

                add_booking = insert(Bookings).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                ).returning(Bookings)
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()


            else:
                return None









