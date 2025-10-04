from fastapi import FastAPI

app = FastAPI(title="MyShop", version="0.0.1")

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


@app.get("/", tags=["Магазин"])
async def home():
    return {"data" : "Welcome to my Shop"}

@app.get("/products", tags=["Продукты"])
async def get_produtcs():
    return {"data" : shop_db}

@app.get("/products/{id}", tags=["Продукты"])
async def get_produtc(id: int):
    if shop_db.get(id, None):
        return {"data" : shop_db[id]}
    else:
        return {"msg" : "Товара не существует"}
    
@app.post("/products/", tags=["Продукты"])
async def add_produtc(data: dict):
    global id_product
    if shop_db.get(id_product, None):
        return {"msg" : "Товар уже существует"}
    else:
        shop_db[id_product] = data
        return {"msg" : data}

@app.put("/products/{id}", tags=["Продукты"])
async def edit_produtc(id: int, data: dict):
    if shop_db.get(id, None):
        shop_db[id] = data
        return {"data" : shop_db[id]}
    else:
        return {"msg" : "Товара не существует"}
