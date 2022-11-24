from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from database.db import Base


class Address(Base):
    """Модель адреса"""
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    street = Column(String(150), nullable=False)
    building = Column(String(30), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    country_id = Column(Integer, ForeignKey("countries.id"))
    city_id = Column(Integer, ForeignKey("cities.id"))
    country = relationship("Country")
    city = relationship("City")

    def __str__(self):
        return f"{self.country_id}, {self.city_id}, {self.street}"

    def __repr__(self):
        return f"{self.country_id}, {self.city_id}, {self.street}"


addresses = Address.__table__
