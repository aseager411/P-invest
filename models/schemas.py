from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserProfile(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True

class User(UserBase):
    id: UUID4
    is_active: bool
    created_at: datetime
    profile: Optional[UserProfile] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
