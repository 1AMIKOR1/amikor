from copy import copy
from typing import Any
from sqladmin import ModelView
from starlette.datastructures import UploadFile
from starlette.requests import Request
from wtforms import FileField
from wtforms.validators import DataRequired

from admin_panel.utils import get_user_data, save_photo, get_current_photo_path, delete_old_photo
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

    def is_accessible(self, request: Request) -> bool:
        # Check user role from session
        user_data = get_user_data(request)
        return user_data.get("role", None) in ["ADMIN"]


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

    def is_accessible(self, request: Request) -> bool:
        # Check user role from session
        user_data = get_user_data(request)
        return user_data.get("role", None) in ["ADMIN"]

class ProductsView(ModelView, model=ProductsModel):
    column_list = [
        ProductsModel.title,
        ProductsModel.price,
        ProductsModel.quantity,
    ]
    name = "Продукт"  # Display name (default: model class name)
    name_plural = "Продукты"  # Plural name (default: name + "s")
    icon = "fa-solid fa-shopping-bag"  # Icon for sidebar
    # category = "Products"  # Group in sidebar
    category_icon = "fa-solid fa-shopping-bag"  # Icon for category
    column_searchable_list = [ProductsModel.title, ProductsModel.price, ProductsModel.quantity]
    form_overrides = dict(photo=FileField)

    form_args = {
        "title": {
            "label": "Название",
            "validators": [DataRequired()]
        },
        "price": {
            "label": "Цена",
            "validators": [DataRequired()]
        },
        "quantity": {
            "label": "Количество",
            "validators": [DataRequired()]
        },
        "photo": {
            "label": "Фото"
        },
        "manufacturer": {
            "label": "Производитель"
        },
    }

    def is_accessible(self, request: Request) -> bool:
        # Check user role from session
        user_data = get_user_data(request)
        return user_data.get("role", None) in ["ADMIN","MANUFACTURER"]


    async def insert_model(self, request: Request, data: dict) -> Any:
        try:
            photo = data.pop("photo", None)
            if photo:
                if isinstance(photo, UploadFile) and photo.filename:  # Проверяем что файл действительно загружен
                    photo_path = await save_photo(photo, "products")
                    data['photo'] = photo_path
                else:
                    data['photo'] = "/static/images/not_found.png"
                return await super().insert_model(request, data)
        except Exception as e:
            print(f"Error in insert_model: {e}")
            raise

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        modified_request = copy(request)
        modified_request.path_params["pk"] = pk
        model = await self.get_object_for_edit(modified_request)
        # Получаем текущее фото записи
        current_photo_path = await get_current_photo_path(model)
        photo = data.get("photo", None)
        # Обрабатываем новое фото
        if photo and isinstance(photo, UploadFile):
            dir_title = "products"
            new_photo_path = await save_photo(photo,dir_title)
            data['photo'] = new_photo_path

            # Удаляем старое фото ЭТОЙ ЖЕ записи
            if current_photo_path:
                await delete_old_photo(current_photo_path, dir_title)
        else:
            data['photo'] = current_photo_path = await get_current_photo_path(model)
        return await super().update_model(request, pk, data)

    async def delete_model(self, request: Request, pk: Any) -> None:
        """Дополнительно: удаляем фото при удалении модели"""
        dir_title = "products"
        modified_request = copy(request)
        modified_request.path_params["pk"] = pk
        model = await self.get_object_for_delete(pk)
        # Получаем текущее фото записи
        current_photo_path = await get_current_photo_path(model)
        if current_photo_path:
            await delete_old_photo(current_photo_path, dir_title)
        try:
            # Удаляем модель
            result = await super().delete_model(request, pk)
            return result
        except Exception as e:
            print(f"Error in delete_model: {e}")
            raise

class ManufacturersView(ModelView, model=ManufacturersModel):
    column_list = [ManufacturersModel.title]
    can_delete = False
    name = "Производитель"  # Display name (default: model class name)
    name_plural = "Производители"  # Plural name (default: name + "s")
    icon = "fa-solid fa-address-card"
    # category = "Products"  # Group in sidebar
    category_icon = "fa-solid fa-shopping-bag"  # Icon for category
    column_searchable_list = [ManufacturersModel.title]

    def is_accessible(self, request: Request) -> bool:
        # Check user role from session
        user_data = get_user_data(request)
        return user_data.get("role", None) in ["ADMIN"]


