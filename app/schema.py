# pydentic schemas
from typing import Optional
import pydantic
from pydantic import EmailStr, Field, conint
from datetime import datetime


class UserCreate(pydantic.BaseModel):
    email: EmailStr
    password: str


class UserOut(pydantic.BaseModel):
    email: EmailStr
    created_at: datetime


class UserLogin(pydantic.BaseModel):
    email: EmailStr
    password: str


class PostBase(pydantic.BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int
    owner: UserOut


class PostCreate(PostBase):
    pass


# Pydentic model for servers response
class ResponsePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True


class Token(pydantic.BaseModel):
    access_token: str
    token_type: str


class TokenData(pydantic.BaseModel):
    id: Optional[str] = None


class Vote(pydantic.BaseModel):
    post_id: int
    dir: int = Field(..., le=1)
