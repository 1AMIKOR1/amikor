from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ManufacturersModel(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))

