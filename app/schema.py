# pydentic schemas
from typing import Optional
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


class UserLogin(pydantic.BaseModel):
    email: EmailStr
    password: str


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    id: Optional[str] = None
