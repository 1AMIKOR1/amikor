from fastapi import APIRouter
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/products", tags=["Продукты"])

from src.schemas.produtcs import SProductAdd
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
async def edit_product(id: int, data: dict):
    if shop_db.get(id, None):
        shop_db[id] = data
        return {"data" : shop_db[id]}
    else:
        return {"msg" : "Товара не существует"}  

@router.patch("/{id}", tags=["Продукты"])
async def edit_partialy_product(id: int, data: dict):
    if shop_db.get(id, None):
        product = shop_db[id]
        for k, v in data.items():
            if product.get(k, None):
                shop_db[id][k] = v

        return {"data" : shop_db[id]}
    else:
        return {"msg" : "Товара не существует"}   

@router.delete("/{id}", tags=["Продукты"])
async def delete_product(id: int):
    if shop_db.get(id, None):
        product = shop_db[id]
        del shop_db[id]        
        return {"msg" : f"{product} был удален"}
    else:
        return {"msg" : "Товара не существует"}   

