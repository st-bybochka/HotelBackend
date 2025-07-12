from pydantic import BaseModel


class HotelsModel(BaseModel):
    id: int
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int

    class Config:
        from_attributes = True


class ShemHotelInfo(BaseModel):
    hotel_name: str
    location: str
    room_name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    hotel_image_id: int
    room_image_id: int

    class Config:
        from_attributes = True
