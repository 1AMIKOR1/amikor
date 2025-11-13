from typing import Any

from sqladmin import ModelView
from starlette.requests import Request
from wtforms import PasswordField, StringField
from sqladmin.forms import Form
from wtforms.validators import DataRequired

from app.models.manufacturers import ManufacturersModel
from app.models.products import ProductsModel
from app.models.roles import RolesModel
from app.models.users import UsersModel
from app.services.auth import AuthService

class RolesView(ModelView, model=RolesModel):
    column_list = [RolesModel.title]
    can_delete = False
    name = "Роль"
    name_plural = "Роли"
    icon = "fa fa-arrows-alt"
    category = "Авторизация"
    category_icon = "fa-solid fa-users"
    column_searchable_list = [RolesModel.title]

class UsersView(ModelView, model=UsersModel):
    column_list = [UsersModel.email, UsersModel.name]
    column_details_exclude_list = [UsersModel.hashed_password]
    can_delete = False
    name = "Пользователь"  # Display name (default: model class name)
    name_plural = "Пользователи"  # Plural name (default: name + "s")
    icon = "fa-solid fa-user"  # Icon for sidebar
    category = "Авторизация"  # Group in sidebar
    category_icon = "fa-solid fa-users"  # Icon for category
    column_searchable_list = [UsersModel.name, UsersModel.email, UsersModel.role]

    form_args = {
        "name": {
            "label": "Имя",
            "validators": [DataRequired()]
        },
        "email": {
            "label" : "Электронная почта"
        },
        "role": {
            "label": "Роль",
            "validators": [DataRequired()]
        },
        "hashed_password": {
            "label": "Пароль",
            "validators": [DataRequired()]
        },
    }


    async def insert_model(self, request: Request, data: dict) -> Any:
        # Обрабатываем пароль перед созданием
        password = data.pop('hashed_password', None)
        if password:
            data['hashed_password'] = AuthService.hash_password(password)
        return await super().insert_model(request, data)

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        # Обрабатываем пароль перед обновлением
        password = data.pop('hashed_password', None)
        if password:
            data['hashed_password'] = AuthService.hash_password(password)
        return await super().update_model(request, pk, data)


class ProductsView(ModelView, model=ProductsModel):
    column_list = [
        ProductsModel.id,
        ProductsModel.manufacturer_id,
        ProductsModel.title,
        ProductsModel.price,
        ProductsModel.quantity,
    ]
    name = "Продукт"  # Display name (default: model class name)
    name_plural = "Продукты"  # Plural name (default: name + "s")
    icon = "fa-solid fa-shopping-bag"  # Icon for sidebar
    # category = "Products"  # Group in sidebar
    category_icon = "fa-solid fa-shopping-bag"  # Icon for category

class ManufacturersView(ModelView, model=ManufacturersModel):
    column_list = [ManufacturersModel.title]
    can_delete = False
    name = "Производитель"  # Display name (default: model class name)
    name_plural = "Производители"  # Plural name (default: name + "s")
    icon = "fa-solid fa-address-card"
    # category = "Products"  # Group in sidebar
    category_icon = "fa-solid fa-shopping-bag"  # Icon for category
    column_searchable_list = [ManufacturersModel.title]