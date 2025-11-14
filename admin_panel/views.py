import shutil
from copy import copy
from datetime import datetime
from pathlib import Path
from typing import Any

import wtforms
from fastapi import UploadFile
from sqladmin import ModelView
from starlette.requests import Request
from wtforms import PasswordField, StringField
from sqladmin.forms import Form
from wtforms.validators import DataRequired

from app.exceptions.auth import InvalidJWTTokenError, InvalidTokenHTTPError, JWTTokenExpiredError, \
    JWTTokenExpiredHTTPError
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
    form_overrides = {
        "photo": wtforms.FileField
    }
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
                if photo.filename:  # Проверяем что файл действительно загружен
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

        # Обрабатываем новое фото
        if 'photo' in data:
            dir_title = "products"
            new_photo = data.pop('photo')
            new_photo_path = await save_photo(new_photo,dir_title)
            data['photo'] = new_photo_path

            # Удаляем старое фото ЭТОЙ ЖЕ записи
            if current_photo_path:
                await delete_old_photo(current_photo_path, dir_title)

        return await super().update_model(request, pk, data)

    async def delete_model(self, request: Request, pk: Any) -> None:
        """Дополнительно: удаляем фото при удалении модели"""
        try:
            modified_request = copy(request)
            modified_request.path_params["pk"] = pk
            model = await self.get_object_for_edit(modified_request)
            # Получаем путь к фото перед удалением
            photo_path = await get_current_photo_path(model)

            # Удаляем модель
            result = await super().delete_model(request, pk)

            # Удаляем файл фото после успешного удаления модели
            if photo_path:
                await delete_old_photo(photo_path, "products")

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


async def save_photo(photo: UploadFile, dir_title: str) -> str:
    """Сохраняет фото и возвращает путь"""
    try:
        # Создаем папку если ее нет
        photo_dir = Path(f"app/static/images/{dir_title}/")
        photo_dir.mkdir(parents=True, exist_ok=True)

        # Генерируем уникальное имя файла
        timestamp = int(datetime.now().timestamp())
        file_extension = Path(photo.filename).suffix if photo.filename else '.webp'
        filename = f"photo_{timestamp}{file_extension}"
        file_path = photo_dir / filename

        # Сохраняем файл
        with open(file_path, "wb+") as buffer:
            shutil.copyfileobj(photo.file, buffer)

        return f"/static/images/{dir_title}/{filename}"

    except Exception as e:
        print(f"Error saving photo: {e}")
        raise

async def delete_old_photo(photo: str, dir_title: str) -> None:
    """Удаляет старое фото если оно существует"""
    try:
        if photo and photo != "":  # Проверяем что путь не пустой
            photo_name = photo.split("/")[-1]
            if photo_name != "not_found.png":
                photo_dir = Path(f"app/static/images/{dir_title}/{photo_name}")
                old_path = photo_dir
                if old_path.exists() and old_path.is_file():
                    old_path.unlink()
    except Exception as e:
        print(f"Error deleting old photo {photo_dir}: {e}")

async def get_current_photo_path(model) -> str | None:
        """Получает текущий путь к фото модели"""
        try:
            if model and hasattr(model, 'photo'):
                current_photo = getattr(model, 'photo', None)
                # Проверяем что это строка и не пустая
                if isinstance(current_photo, str) and current_photo.strip():
                    return current_photo
        except Exception as e:
            print(f"Error getting current photo path: {e}")
        return None
def get_user_data(request: Request):
    try:
        token = request.session.get('access_token')
        return AuthService.decode_token(token)
    except InvalidJWTTokenError:
        raise InvalidTokenHTTPError
    except JWTTokenExpiredError:
        request.session.clear()
        raise JWTTokenExpiredHTTPError