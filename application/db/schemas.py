from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class QouteBase(BaseModel):
    qoute: str
    author: str
    number: int
    blockqoute: str


class QouteCreate(QouteBase):
    pass


class Qoute(QouteBase):
    id: int

    class Config:
        orm_mode = True


class AccessLogBase(BaseModel):
    pass


class AccessLogCreate(AccessLogBase):
    user_id: int


class AccessLog(AccessLogBase):
    user_id: int
    time_stamp: datetime
