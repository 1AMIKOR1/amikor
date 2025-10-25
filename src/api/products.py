from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/products", tags=["Продукты"])

from src.schemas.produtcs import SProductAdd, SProductPatch
from src.repositories.produtcs import ProductsRepository
from src.database import async_session_maker
shop_db ={
    0 : {
        "name" : "Шампунь",
        "quantity": 3,
        "price" : 50
    },
    1 : {
        "name" : "Пицца",
        "quantity": 30,
        "price" : 500
    },
    2 : {
        "name" : "Вода",
        "quantity": 10,
        "price" : 50
    },
}

count:int = 3

@router.get("/")
async def get_products():
    async with async_session_maker() as session:
        data = await ProductsRepository(session).get_filtered()
    return {"data" : data}

@router.get("/{id}", tags=["Продукты"])
async def get_product(id: int):
    async with async_session_maker() as session:
        data = await ProductsRepository(session).get_one_or_none(id=id)
    if data:
        return {"data" : data}
    else:
        return {"msg" : "Товара не существует"}

@router.post("/", tags=["Продукты"])
async def add_product(product: SProductAdd):
    async with async_session_maker() as session:
        try:
            await ProductsRepository(session).add(product)
        except IntegrityError:
            return {"msg" : "Такой товар существует"}
        await session.commit()
    return {"Данные успешно добавлены!"}
    
@router.put("/{id}", tags=["Продукты"])
async def edit_product(id: int, data: SProductAdd):
    async with async_session_maker() as session:
        product = await ProductsRepository(session).get_one_or_none(id=id)
        if product:
            await ProductsRepository(session).edit(data, id=id)
            await session.commit()
            return {"msg" : "Данные обновлены!"}
        
        return {"msg" : "Товара не существует"}  

@router.patch("/{id}", tags=["Продукты"])
async def edit_partialy_product(id: int, data: SProductPatch):
    async with async_session_maker() as session:
        product = await ProductsRepository(session).get_one_or_none(id=id)
        if product:
            (
                await ProductsRepository(session)
                .edit(data, exclude_unset=True, id=id)
            )
            await session.commit()
            return {"msg" : "Данные обновлены!"}
        
        return {"msg" : "Товара не существует"}  

@router.delete("/{id}", tags=["Продукты"])
async def delete_product(id: int):
    async with async_session_maker() as session:
        product = await ProductsRepository(session).get_one_or_none(id=id)
        if product:
            await ProductsRepository(session).delete(id=id)
            await session.commit()
            return {"msg" : f"{product} был удален"}
        
        return {"msg" : "Товара не существует"}   

