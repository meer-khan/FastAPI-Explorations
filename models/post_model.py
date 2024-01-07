from pydantic import BaseModel, Strict, Field
from typing import Optional

class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = Field(strict=True, default=None) 