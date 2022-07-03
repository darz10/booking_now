from sqlalchemy import Column, String, Integer, ForeignKey, Time, Enum, Date
from sqlalchemy.orm import relationship

from database.db import Base
from institutions.enums import CelebrationType

class Reservation(Base):
    """Модель бронирования стола"""
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True)
    amount_guests = Column(Integer)
    date_reservation = Column(Date)
    time_start = Column(Time(timezone=True), nullable=False)
    time_end = Column(Time(timezone=True), nullable=False)
    celebration = Column(Enum(CelebrationType))
    note = Column(String(length=300))
    user_id = Column(Integer, ForeignKey("users.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    user = relationship("User")
    table = relationship("Table")

    def __str__(self):
        return f"{self.date_reservation} {self.time_start} - {self.time_end} table_id: {self.table_id}"


reservations = Reservation.__table__