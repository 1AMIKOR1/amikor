import shutil
from datetime import datetime
from pathlib import Path

from starlette.datastructures import UploadFile
from starlette.requests import Request

from app.exceptions.auth import InvalidJWTTokenError, JWTTokenExpiredError, InvalidTokenHTTPError, \
    JWTTokenExpiredHTTPError
from app.services.auth import AuthService


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