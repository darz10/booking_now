from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class PlaceType(Base):
    """Модель типа места места(ресторан, бар и.тп)"""
    __tablename__ = "place_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    places = relationship("Place")

    def __str__(self):
        return f"PlaceType: {self.title}"


place_types = PlaceType.__table__
