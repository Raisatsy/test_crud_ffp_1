from pydantic import BaseModel, EmailStr, constr
from typing import Optional


class User(BaseModel):
    name: constr(max_length=20)
    surname: constr(max_length=20)
    email: EmailStr
    user_id: int


class UserUpdate(BaseModel):
    name: Optional[constr(max_length=20)] = None
    surname: Optional[constr(max_length=20)] = None
    email: Optional[EmailStr] = None
