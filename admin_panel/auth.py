from fastapi import HTTPException
from jwt import ExpiredSignatureError
from pydantic import ValidationError
from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.requests import Request

from app.api.dependencies import get_db
from app.exceptions.auth import UserNotFoundError, UserNotFoundHTTPError, InvalidPasswordError, \
    InvalidPasswordHTTPError, NoAccessTokenHTTPError, JWTTokenExpiredHTTPError, JWTTokenExpiredError
from app.schemas.users import SUserAuth
from app.services.auth import AuthService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        try:
            user_data = SUserAuth(email=form["username"], password=form["password"])
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e) from e
        async for db in get_db():
            try:
                access_token: str = await AuthService(db).login_user(user_data)
                request.session.update({"access_token": access_token})
                return True
            except UserNotFoundError:
                raise UserNotFoundHTTPError
            except InvalidPasswordError:
                raise InvalidPasswordHTTPError



    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        try:
            token = request.session.get('access_token')
            if not token:
                raise NoAccessTokenHTTPError
        except JWTTokenExpiredError:
            request.session.clear()
            raise JWTTokenExpiredHTTPError
        return True


authentication_backend = AdminAuth(secret_key="your_secret_key")

