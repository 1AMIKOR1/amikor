from fastapi import FastAPI
from sqladmin import Admin
from starlette.staticfiles import StaticFiles

from admin_panel.admin import CustomAdmin
from admin_panel.auth import authentication_backend
from admin_panel.views import ManufacturersView, UsersView, ProductsView, RolesView
from app.api.auth import router as auth_router
from app.database.database import engine

app = FastAPI(title="MyShop", version="0.0.1")
app.mount('/static', StaticFiles(directory='app/static'), 'static')

@app.get("/", tags=["Магазин"])
async def home():
    return {"data": "Welcome to my Shop"}


app.include_router(auth_router)

admin = CustomAdmin(
    app,
    engine,
    authentication_backend=authentication_backend,
    title="Админ панель",
    templates_dir="admin_panel/templates",
)

admin.add_view(UsersView)
admin.add_view(ProductsView)
admin.add_view(ManufacturersView)
admin.add_view(RolesView)
