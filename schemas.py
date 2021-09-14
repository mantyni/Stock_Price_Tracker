from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class User(UserBase):
    id: int
    email: str

    class Config:
        orm_mode = True


class GetUser(BaseModel):
   email: str
