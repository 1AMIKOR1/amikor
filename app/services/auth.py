from datetime import datetime, timezone, timedelta

from app.config import settings
from app.exceptions.auth import (
    UserAlreadyExistsError,
    UserNotFoundError,
    InvalidPasswordError,
)
from app.exceptions.base import ObjectAlreadyExistsError
from app.schemas.users import SUserAdd, SUserAddRequest, SUserGet
from app.services.base import BaseService
import jwt
from passlib.context import CryptContext


class InvalidJWTTokenError:
    pass


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_access_token(cls, data: dict) -> str:
        to_encode = data.copy()
        expire: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    @classmethod
    def verify_password(cls, plain_password, hashed_password) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, plain_password) -> str:
        return cls.pwd_context.hash(plain_password)

    @classmethod
    def decode_token(cls, token: str) -> dict:
        try:
            return jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        except jwt.exceptions.DecodeError as ex:
            raise InvalidJWTTokenError from ex

    async def register_user(self, user_data: SUserAddRequest):
        # user = await self.db.users.get_one_or_none(email=user_data.email)
        # if user:
        #     raise UserAlreadyExistsError
        try:
            hashed_password: str = self.hash_password(user_data.password)
            new_user_data = SUserAdd(
                email=user_data.email,
                hashed_password=hashed_password,
                name=user_data.name,
            )
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsError:
            raise UserAlreadyExistsError

    async def login_user(self, user_data: SUserAddRequest):
        user = await self.db.users.get_one_or_none(email=user_data.email)
        if not user:
            raise UserNotFoundError
        if not self.verify_password(user_data.password, user.hashed_password):
            raise InvalidPasswordError
        access_token: str = self.create_access_token(
            {
                "user_id": user.id,
                "role": user.role_id,
            }
        )
        return access_token

    async def get_me(self, user_id: int):
        user: None | SUserGet = await self.db.users.get_one_or_none(id=user_id)
        if not user:
            raise UserNotFoundError
        return user
