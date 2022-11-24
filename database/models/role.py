from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class Role(Base):
    """Модель роли пользователя"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    users = relationship("User")


roles = Role.__table__
