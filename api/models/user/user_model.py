import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from beanie import Document, Indexed
from bson.objectid import ObjectId
from pydantic import AnyHttpUrl, BaseModel, EmailStr, Field

class UserModel(Document):
    """User student model to database document."""

    register_date: datetime.datetime = datetime.datetime.now()
    refresh_token: str = ''
    is_account_active: bool = False
    is_banned: bool = False
    token: Optional[str] = ''
    user_id: Indexed(str, unique=True)

    fname: str
    lname: str
    email: str
    password: str
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    city: Optional[str]
    district: Optional[str]
    state: Optional[str]
    pin_code: Optional[str]

    class Collection:
        name  = "users"