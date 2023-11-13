import uuid
from fastapi_users import schemas
from typing import Optional
class UserRead(schemas.BaseUser[uuid.UUID]):
    email: str
    username: str
    address:str 
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    address:str 
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: str
    password: str
    address:str 
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False