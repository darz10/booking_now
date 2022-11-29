from typing import List, Optional
from sqlalchemy import update, insert, select
from databases import Database

from settings import settings
from database.models import User
from database.repository import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: User):
        self.db_connection = db_connection
        self.db_model = db_model

    async def create(
        self,
        first_name: str,
        phone_number: str,
        last_name: Optional[str],
        password: Optional[str],
        email: Optional[str],
        role_id: int = settings.USER_DEFAULT_ROLE,
        is_active: bool = True
    ):
        try:
            new_user = insert(self.db_model(
                first_name=first_name,
                role_id=role_id,
                phone_number=str(phone_number),
                last_name=last_name,
                password=password,
                email=email,
                is_active=is_active))

            user = await self.db_connection.execute(new_user)
            return user
        except Exception as exc:
            print("Error method db create in UserRepository", exc)

    async def all(self) -> List[User]:
        places = await self.db_connection.fetch_all(
            query=select(self.db_model)
        )
        return places

    async def get(self, id: int) -> User:
        user = await self.db_connection.fetch_one(
            query=select(self.db_model).where(self.db_model.id == id)
        )
        return user

    async def update(self, id: int, *args, **kwargs) -> User:
        user = update(self.db_model).where(self.db_model.id == id)
        user = user.values(**kwargs)
        return await self.db_connection.fetch_one(user)

    async def delete(self, id: int) -> None:
        user = update(self.db_model).where(self.db_model.id == id)
        user.values(is_active=False)
        user.execution_options(synchronize_session="fetch")
        return await self.db_connection.execute(user)

    async def get_user_by_phone(self, phone_number: str) -> User:
        user = await self.db_connection.fetch_one(
            select(self.db_model).where(
                self.db_model.phone_number == phone_number
            )
        )
        return user
