# pydentic schemas
import pydantic
from pydantic import EmailStr
from datetime import datetime


class PostBase(pydantic.BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


# Pydentic model for servers response
class ResponsePost(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserCreate(pydantic.BaseModel):
    email: EmailStr
    password: str


class UserOut(pydantic.BaseModel):
    email: EmailStr
    created_at: datetime
