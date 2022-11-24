from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database.db import Base


class UserPlace(Base):
    """Модель описывающаю связь пользователя с заведением"""
    __tablename__ = "user_places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    place_branch_id = Column(Integer, ForeignKey("place_branches.id"))
    is_favourite = Column(Boolean, default=False)
    branch = relationship("PlaceBranch")

    def __str__(self):
        return f"{self.user_id}, {self.place_branch_id}"


user_places = UserPlace.__table__
