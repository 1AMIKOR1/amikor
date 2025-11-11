from fastapi import HTTPException
from pydantic import ValidationError
from sqladmin.authentication import AuthenticationBackend
from starlette import status
from starlette.requests import Request


from app.users.auth import authenticate_user, create_access_token
from app.users.schemas import SUserAuth


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        form = await request.form()
        try:
            user_data = SUserAuth(email=form["username"], password=form["password"])
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=e.message) from e
        user = await authenticate_user(email=user_data.email, password=user_data.password)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid user")
        if user.is_super_admin:
            access_token = create_access_token({"sub": str(user.id)})
            request.session.update({"users_access_token": access_token})
            return True
        raise HTTPException(status_code=403, detail="Access denied")

    async def logout(self, request: Request):
        request.session.clear()
        return True

    async def authenticate(self, request):
        token = request.session.get('users_access_token')
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token not found')
        return True


authentication_backend = AdminAuth(secret_key="your_secret_key")

