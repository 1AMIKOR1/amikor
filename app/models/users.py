from enum import Enum

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class UsersRoles(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    MANUFACTURER = "MANUFACTURER"

class UsersModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    name: Mapped[str] = mapped_column(String(50))
    hash_password: Mapped[str] = mapped_column(String(50))
    role: Mapped[UsersRoles] = mapped_column(String(50),default=UsersRoles.USER,)

