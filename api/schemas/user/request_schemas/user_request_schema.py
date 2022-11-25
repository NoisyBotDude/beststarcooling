from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class UserRegisterSchema(BaseModel):
    user_id: str
    fname: str
    lname: str
    email: str
    password: str
    
class UserLoginSchema(BaseModel):
    email: str
    password: str
    
class UserUpdateSchema(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class SendFormRequestSchema(BaseModel):
    fname: str
    lname: str
    phone: str
    email: str
    address_line_1: str
    address_line_2: str
    city: str
    district: str
    state: str
    pin_code: str

class UpdateFormRequestSchema(BaseModel):
    fname: Optional[str] = None
    lname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    pin_code: Optional[str] = None

