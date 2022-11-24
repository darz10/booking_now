import logging
import json
from typing import List, Optional, Tuple

from sqlalchemy import update, delete, select, insert
from sqlalchemy.sql.elements import BinaryExpression 
from databases import Database
from databases.backends.postgres import Record

from database.models import Place
from database.repository import AbstractRepository


class PlaceRepository(AbstractRepository):
    def __init__(self, db_connection: Database, db_model: Place):
        self.db_connection = db_connection
        self.db_model = db_model
        self._operator_map = {
            None: lambda attr, value: attr.op("=")(value),  # k:v - k=v
            "eq": lambda attr, value: attr.op("=")(value),  # k__eq:v - k=v
            "gt": lambda attr, value: attr.op(">")(value),  # k__gt:v - k>v
            "gte": lambda attr, value: attr.op(">=")(value),  # k__gte:v - k>=v
            "in": lambda attr, value: attr.in_(
                json.loads(value)
            ),  # k__in:v - k in v
            "lt": lambda attr, value: attr.op("<")(value),  # k__lt:v - k<v
            "lte": lambda attr, value: attr.op("<=")(value),  # k__lte:v - k<=v
            "ne": lambda attr, value: attr.op("!=")(value),  # k__ne:v - k!=v
            "ilike": lambda attr, value: attr.like(
                f"%{value}%"
            ),  # k__regex:v k contains v
        }

    async def create(
        self,
        title: str,
        user_id: int,
        place_type: int,
        place_description: Optional[str] = None,
        url: Optional[str] = None,
        avatar: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
    ) -> Record:
        new_place = insert(self.db_model).values(
            title=title,
            place_description=place_description,
            url=url,
            avatar=avatar,
            email=email,
            phone=phone,
            place_type=place_type,
            user_id=user_id,
        ).returning(self.db_model)
        return await self.db_connection.fetch_one(new_place)

    async def all(self) -> List[Record]:
        places = await self.db_connection.fetch_all(
            query=select(self.db_model)
        )
        return places

    async def get(self, id: int) -> Record:
        place = await self.db_connection.fetch_one(
            query=select(self.db_model).where(self.db_model.id == id)
        )
        return place

    async def update(self, id: int, *args, **kwargs) -> Record:
        place = update(self.db_model).where(self.db_model.id == id)
        # TODO сделать через цикл, иначе придётся править каждый раз
        if kwargs.get("title"):
            place = place.values(title=kwargs["title"])
        if kwargs.get("type_place"):
            place = place.values(type_place=kwargs["type_place"])
        if kwargs.get("avatar"):
            place = place.values(avatar=kwargs["avatar"])
        if kwargs.get("description"):
            place = place.values(description=kwargs["description"])
        if kwargs.get("url"):
            place = place.values(url=kwargs["url"])
        if kwargs.get("email"):
            place = place.values(email=kwargs["email"])
        if kwargs.get("phone"):
            place = place.values(phone=kwargs["phone"])
        return await self.db_connection.execute(place)

    async def delete(self, id: int) -> None:
        """Удаление места с возвратом статуса, True(объект удалён)"""
        place = delete(self.db_model).where(
            self.db_model.id == id
        ).returning(self.db_model.id)
        deleted_place = await self.db_connection.execute(place)
        return deleted_place.all()

    async def filter(self, *args, **kwargs) -> List[Record]:
        formated_filters = self.formation_fitlers_database(*args)
        places = await self.db_connection.fetch_all(
            select(self.db_model).where(*formated_filters))
        return places

    def formation_fitlers_database(self, filters) -> List[BinaryExpression]:
        """
        Формирование фильтров запроса БД.
        Пока сделано для формирования фильтров по
        типу `title__ilike`
        """
        queries = []
        for filter in filters:
            raw_filter_query, value = filter            
            self.parse_operator(raw_filter_query, value)
        return queries

    def parse_operator(self, key: str, value: str):
        """
        BinaryExpression
        eg. x__gt:30 -> filter(x >= 30 )
        eg. x__in:[1,2,3] -> filter(x.in_([1,2,3]))
        """
        if "__" in key:
            field, _operator = key.split("__")
        else:
            _operator = None
            attr_name = key
        model_field = getattr(self.db_model, field, None)
        if not model_field:
            raise ValueError("unknown field {}".format(attr_name))
        if _operator not in self._operator_map:
            raise ValueError("unknown operator {}".format(key))
        return self._operator_map[_operator](model_field, value)
