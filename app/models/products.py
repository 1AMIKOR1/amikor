from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from app.database import Base

if TYPE_CHECKING:
    from app.models.manufacturers import ManufacturersModel
    
class ProductsModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacture_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    quantity: Mapped[int]

    manufacturer: Mapped["ManufacturersModel"] = relationship(
        back_populates="products",

    )
 