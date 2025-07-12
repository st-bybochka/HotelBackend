from fastapi import HTTPException, status

UserAlreadyExistsError = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists"
)

IncorrectEmailOrPasswordError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password"
)

TokenExpiredError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token expired"
)

TokenAbsentError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token absent"
)


TokenIncorrectError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token incorrect"
)

RoomCannotBookedError = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Room cannot booked"
)