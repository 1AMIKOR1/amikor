from fastapi import FastAPI

app = FastAPI(title="MyShop", version="0.0.1")



@app.get("/", tags=["Магазин"])
async def home():
    return {"data" : "Welcome to my Shop"}

