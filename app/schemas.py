from pydantic import BaseModel, Strict, Field, EmailStr
from typing import Optional
from datetime import datetime
class PostBase(BaseModel):
    title: str 
    content: str
    published: bool = True
    # rating: Optional[int] = Field(strict=True, default=None) 

class Post(PostBase):
    id: int
    # title: str 
    # content: str
    # published: bool = True
    created_at : datetime


class UserCreate(BaseModel): 
    email: EmailStr
    password: str 
    # @model_validator(mode='after')
    # def check_passwords_match(self) -> 'UserModel':
    #     pw1 = self.password1
    #     pw2 = self.password2
    #     if pw1 is not None and pw2 is not None and pw1 != pw2:
    #         raise ValueError('passwords do not match')
    #     return self

    # @root_validator()
    # def verify_password_match(cls,values):
    #     password = values.get("password")
    #     confirm_password = values.get("confirm_password")

    #     if password != confirm_password:
    #         raise ValueError("The two passwords did not match.")
    #     return values

class UserOut(UserCreate): 
    id:int
    email: EmailStr

    # class Config:
    #     orm_mode = True
    