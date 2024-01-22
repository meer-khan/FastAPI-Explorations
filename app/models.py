from database import Base , Integer
from sqlalchemy import Column
from typing import List
from sqlalchemy import ForeignKey
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


# Following SQLALCHEMY 2.0 Documentation
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html
class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
