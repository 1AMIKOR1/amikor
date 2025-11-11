from fastapi import FastAPI
from sqladmin import Admin

# from admin_panel.auth_admin_panel import authentication_backend
from admin_panel.views import UsersView, ProductsView
from app.api.auth import router as auth_router
from app.database.database import engine

app = FastAPI(title="MyShop", version="0.0.1")


@app.get("/", tags=["Магазин"])
async def home():
    return {"data": "Welcome to my Shop"}


app.include_router(auth_router)

admin = Admin(
    app,
    engine,
    # authentication_backend=authentication_backend,
    title="Админ панель",
    templates_dir="admin_panel/templates",
)
admin.add_view(UsersView)
admin.add_view(ProductsView)
