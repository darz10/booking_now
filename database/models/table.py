from sqlalchemy import Column, Integer, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship

from database.db import Base


class Table(Base):
    """Модель стола заведения"""
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    is_favourite = Column(Boolean, default=False)
    table_number = Column(Integer, nullable=False)
    max_people = Column(Integer, nullable=False)
    is_electricity = Column(Boolean, default=False)
    floor = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True)
    place_branch_id = Column(Integer, ForeignKey("place_branches.id"))
    reservations = relationship("Reservation")


    __table_args__ = (UniqueConstraint('table_number', 'place_branch_id', name='_table_place_branch_unique'),
                     )

    def __str__(self):
        return f"{self.place_branch_id} {self.table_number} {self.is_available}"


tables = Table.__table__