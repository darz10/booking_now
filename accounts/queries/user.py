from typing import List, Optional
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from settings import settings
from database.models import User
from database.repository import AbstractRepository


class UserRepository(AbstractRepository):
    def __init__(self, db_session: Session, db_model: User):
        self.db_session = db_session
        self.db_model = db_model

    async def user_updated(self, first_name: str, phone_number: str, 
                          last_name: Optional[str], password: Optional[str], 
                          email: Optional[str], role_id: int=settings.USER_DEFAULT_ROLE,
                          is_active: bool = True):
        try:
            new_user = self.db_model(first_name=first_name, 
                                    role_id=role_id, 
                                    phone_number=str(phone_number), 
                                    last_name=last_name,
                                    password=password, 
                                    email=email,
                                    is_active=is_active)
            self.db_session.add(new_user)
            await self.db_session.flush()
            return new_user
        except Exception as exc:
            print("Error method db user_updated", exc)

    async def get_all(self) -> List[User]:
        places = await self.db_session.execute(select(self.db_model).order_by(self.db_model.id))
        return places.scalars().all()

    async def get_user(self, id: int) -> User:
        user = await self.db_session.execute(select(self.db_model).where(self.db_model.id == id))
        return user.scalars().all()

    async def update_user(self, id: int, first_name: Optional[str],
                          last_name: Optional[str], password: Optional[str],
                          phone_number: Optional[str], email: Optional[str],
                          is_active: Optional[bool]=None, role_id: Optional[int]=None) -> None:
        user = update(self.db_model).where(self.db_model.id == id)
        if first_name:
            user = user.values(first_name=first_name)
        if last_name:
            user = user.values(last_name=last_name)
        if password:
            user = user.values(password=password) 
        if phone_number:
            user = user.values(phone_number=phone_number) 
        if is_active:
            user = user.values(is_active=is_active) 
        if role_id:
            user = user.values(role_id=role_id)
        if email:
            user = user.values(email=email)
        user.execution_options(synchronize_session="fetch")
        return await self.db_session.execute(user)

    async def get_user_by_phone(self, phone_number: str) -> User:
        user = await self.db_session.execute(select(self.db_model).where(self.db_model.phone_number == phone_number))
        return user.scalars().one()