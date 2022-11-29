from pydantic import BaseModel


class BaseFilter(BaseModel):
    @property
    def has_objects(self):
        values = self.dict().values()
        return any(values)
