from pydantic import BaseModel, Strict, Field
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
