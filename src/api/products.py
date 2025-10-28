from fastapi import APIRouter

from src.repositories.products import ProductsRepository
from src.database import async_session_maker

router = APIRouter(prefix="/products", tags=["Продукты"])

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

id_product = 3

@router.get("/", tags=["Продукты"])
async def get_produtcs():
    return {"data" : shop_db}

@router.get("/{id}", tags=["Продукты"])
async def get_product(id: int):
    async with async_session_maker() as session:
        data = await ProductsRepository(session).get_one_or_none(id=id)
    if data:
        return {"data" : data}
    else:
        return {"msg" : "Товара не существует"}
    
@router.post("/", tags=["Продукты"])
async def add_product(data: dict):
    global id_product
    id: int = id_product
    if shop_db.get(id, None):
        shop_db[id] = data
        id_product += 1
        return {"msg" : "Данные добавлены"}
    else:
        return {"err" : "Такой товар существует!"}

@router.delete("/{id}", tags=["Продукты"])
async def delete_product(id: int):
    if shop_db.get(id, None):
        del shop_db[id]
        return {"msg" : f"Товар с id: {id} удален"}
    return {"err" : "Такой товар не существует!"}

@router.put("/{id}", tags=["Продукты"])
async def edit_product(id:int, data: dict):
    if shop_db.get(id, None):
        shop_db[id] = data
        return {"msg" : f"Товар с id: {id} обновлен"}
    return {"err" : "Такой товар не существует!"}

@router.patch("/{id}", tags=["Продукты"])
async def edit_product_partialy(id:int, data: dict):
    if shop_db.get(id, None):
        product = shop_db[id]
        for k, v in data.items():
            if product.get(k, None):
                shop_db[id][k] = v
                
        return {"msg" : f"Товар с id: {id} обновлен"}
    
    return {"err" : "Такой товар не существует!"}