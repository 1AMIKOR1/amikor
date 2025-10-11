import logging

from aiosqlite import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_all_with_paging(self, limit: int, offset: int):
        query = select(self.model).limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_filtered(
        self,
        *filter,
        **filter_by,
    ):
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        filter_ = [v for v in filter if v is not None]

        query = select(self.model).filter(*filter_).filter_by(**filter_by)
        result = await self.session.execute(query)

        return [
            self.schema.model_validate(model, from_attributes=True)
            for model in result.scalars().all()
        ]

    async def get_all(self) -> list[BaseModel]:
        return await self.get_filtered()

    async def add(self, data: BaseModel):
        try:
            add_stmt = (
                insert(self.model)
                .values(**data.model_dump())
                .returning(self.model)
            )
            result = await self.session.execute(add_stmt)
            model = result.scalars().one()
            return self.schema.model_validate(model, from_attributes=True)

        except IntegrityError as ex:
            logging.error(
                "Не удалось добавить данные в БД тип ошибки:%s",
                type(ex.orig.__cause__),
            )
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ex
            logging.error(
                "незнакомая ошибка: тип ошибки:%s", type(ex.orig.__cause__)
            )
            raise ex

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)

        result = await self.session.execute(query)

        model = result.scalars().one_or_none()
        if model is None:
            return None

        return self.schema.model_validate(model, from_attributes=True)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        edit_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(
                **data.model_dump(
                    exclude_unset=exclude_unset, exclude_none=exclude_unset
                )
            )
        )
        await self.session.execute(edit_stmt)