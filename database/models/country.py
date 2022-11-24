from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base


class Country(Base):
    """Модель страны"""
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    cities = relationship("City")

    def __str__(self):
        return f"Country: {self.name}"


countries = Country.__table__
