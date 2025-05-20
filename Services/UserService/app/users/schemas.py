import uuid
from fastapi_users import schemas
from pydantic import EmailStr ,field_validator
from typing import Optional
from datetime import datetime
class UserRead(schemas.BaseUser[uuid.UUID]):
    email: EmailStr
    username: str
    registered_at: datetime
    address:str 
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    address:str 
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if not any(char in "!@#$%^&*()_+-=[]{}|;':\",.<>/?`~" for char in v):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return v


class UserUpdate(schemas.BaseUserUpdate):
    username: Optional[str]
    email:  Optional[EmailStr] 
    password: Optional[str]
    address: Optional[str]
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Пароль должен содержать минимум 8 символов")
        if not any(char in "!@#$%^&*()_+-=[]{}|;':\",.<>/?`~" for char in v):
            raise ValueError("Пароль должен содержать хотя бы один специальный символ")
        return v