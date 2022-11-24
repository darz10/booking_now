from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    JSON,
    Boolean,
    DateTime
)
from sqlalchemy.sql import func


from database.db import Base


class MediaFile(Base):
    """Модель медиа файла c полями для загрузки в S3"""
    __tablename__ = "media_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_id = Column(String(150), nullable=False)
    source_fields = Column(JSON)
    source_url = Column(String(200))
    uploaded = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    filename = Column(String(250), nullable=False)
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __str__(self):
        return f"{self.filename}, {self.user}"

    def __repr__(self):
        return f"File: {self.filename} Owner: {self.user}"


mediafiles = MediaFile.__table__
