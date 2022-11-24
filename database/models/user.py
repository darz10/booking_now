from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import relationship

from database.db import Base


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint(
            "phone_number",
            "email",
            name='unique_component_user'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100))
    password = Column(String(100))
    phone_number = Column(String(12), nullable=False)
    email = Column(String(100))
    is_active = Column(Boolean, default=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")
    reservations = relationship("Reservation")

    def __str__(self):
        return f"{self.first_name} - {self.phone_number}"
