from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database.database import Base



class ProductsModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer_id: Mapped[int] = mapped_column(ForeignKey("manufacturers.id"))
    title: Mapped[str] = mapped_column(String(100))
    price: Mapped[int]
    quantity: Mapped[int]
    photo: Mapped[str | None] = mapped_column(String(100), default= None)
    manufacturer = relationship("ManufacturersModel")
