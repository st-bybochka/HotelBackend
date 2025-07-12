from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

from app.user.router import router as user_router
from app.booking.router import router as booking_router
from app.hotel.router import router as hotel_router

app = FastAPI(
    title="HotelProjectRro_v2.0",
    description="API for HotelProjectRro_v2.0",
    version="1.0.0"
)
app.include_router(user_router)
app.include_router(booking_router)
app.include_router(hotel_router)


@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")