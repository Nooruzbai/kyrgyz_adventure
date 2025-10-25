from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from typing import List


class Base(DeclarativeBase):
    pass