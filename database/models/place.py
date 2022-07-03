from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database.db import Base
from institutions.enums import PlaceType


class Place(Base):
    """Модель заведения"""
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(String(250))
    url = Column(String(150))
    avatar = Column(String(250))
    email = Column(String(100))
    phone = Column(String(15))
    type_place = Column(Enum(PlaceType))
    user_id = Column(Integer, ForeignKey("users.id"))
    branches = relationship("PlaceBranch")
    places_media_files = relationship("PlaceMediaFile")

    def __str__(self):
        return f"{self.title}, {self.phone}, {self.type_place}"


places = Place.__table__