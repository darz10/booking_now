from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    def __init__(self, db_session):
        self.db_session = db_session

    @abstractmethod
    def get(self, id: int):
        raise NotImplementedError()

    @abstractmethod
    def list(self):
        raise NotImplementedError()

    @abstractmethod
    def create(self, obj):
        raise NotImplementedError()

    @abstractmethod
    def update(self, id: int, obj):
        raise NotImplementedError()

    @abstractmethod
    def delete(self, id: int):
        raise NotImplementedError()
