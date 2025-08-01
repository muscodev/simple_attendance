from pydantic import BaseModel


class Coordinate(BaseModel):
    lat: float = None
    lon: float = None


class LoginPost(BaseModel):
    username: str
    password: str
