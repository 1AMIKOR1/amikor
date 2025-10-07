from fastapi import APIRouter

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

router = APIRouter(prefix="/products", tags=["Продукты"])


@router.get("/")
async def get_produtcs():
    return {"data" : shop_db}

@router.get("/")
async def get_produtcs():
    return {"data" : shop_db}


@router.post("/")
async def add_produtc(data: dict):
    global id_product
    if shop_db.get(id_product, None):
        return {"msg" : "Товар уже существует"}
    else:
        shop_db[id_product] = data
        return {"msg" : data}

@router.get("/{id}")
async def get_produtc(id: int):
    if shop_db.get(id, None):
        return {"data" : shop_db[id]}
    else:
        return {"msg" : "Товара не существует"}
    
@router.put("/{id}")
async def edit_produtc(id: int, data: dict):
    if shop_db.get(id, None):
        shop_db[id] = data
        return {"data" : shop_db[id]}
    else:
        return {"msg" : "Товара не существует"}
    
@router.patch("/{id}")
async def edit_partialy_produtc(id: int, data: dict):
    if shop_db.get(id, None):
        product = shop_db[id]
        for k, v in data.items():
            if product.get(k, None):
                shop_db[id][k] = v
        return {"msg" : "Товар обновлен!"}
    else:
        return {"msg" : "Товара не существует"}


@router.delete("/{id}")
async def delete_produtc(id: int):
    if shop_db.get(id, None):
        del shop_db[id]
        return {"msg" : "Товар удален"}
    else:
        return {"msg" : "Товара не существует"}



