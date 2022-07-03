from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base


class City(Base):
    """Модель города"""
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"))
    country = relationship("Country")


    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"City: {self.name}"


cities = City.__table__