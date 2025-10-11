from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.manufacturers import ProdutcsModel

class ManufacturersModel(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))

    produts: Mapped[list["ProdutcsModel"]] = relationship(
        back_populates="products"

    )
 