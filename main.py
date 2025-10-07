from fastapi import FastAPI
from app.api.products import router as products_router

app = FastAPI(title="MyShop", version="0.0.1")

@app.get("/", tags=["Магазин"])
async def home():
    return {"data" : "Welcome to my Shop"}

app.include_router(products_router)



