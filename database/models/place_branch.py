from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class PlaceBranch(Base):
    """Модель точки компании"""
    __tablename__ = "place_branches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places.id"))
    place_address_id = Column(Integer, ForeignKey("addresses.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    place = relationship("Place")
    address = relationship("Address")
    user_places = relationship("UserPlace")

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street}"


place_branches = PlaceBranch.__table__
