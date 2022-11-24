from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


from database.db import Base


class PlaceMediaFile(Base):
    """Модель связи заведения с медиа файлами"""
    __tablename__ = "place_media_files"

    id = Column(Integer, primary_key=True, autoincrement=True)
    place_id = Column(Integer, ForeignKey("places.id"))
    file_id = Column(Integer, ForeignKey("media_files.id"))
    media_file = relationship("MediaFile")
    place = relationship("Place")

    def __str__(self):
        return f"{self.place}, {self.file}"


place_media_files = PlaceMediaFile.__table__
