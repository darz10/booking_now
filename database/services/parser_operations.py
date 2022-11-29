import json
from typing import List

from sqlalchemy.sql.elements import BinaryExpression


def _get_operator_map():
    operations = {
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
    return operations


def parse_operator(key: str, value: str, db_model):
    """
    Конвертирование фильтра запроса в
    фильтр запроса к БД
    BinaryExpression
    eg. x__gt:30 -> filter(x >= 30 )
    eg. x__in:[1,2,3] -> filter(x.in_([1,2,3]))
    """
    if "__" in key:
        field, _operator = key.split("__")
    else:
        _operator = None
        attr_name = key
    model_field = getattr(db_model, field, None)
    if not model_field:
        raise ValueError("unknown field {}".format(attr_name))
    if _operator not in _get_operator_map():
        raise ValueError("unknown operator {}".format(key))
    return _get_operator_map()[_operator](model_field, value)


def formation_fitlers_database(db_model, filters) -> List[BinaryExpression]:
    """
    Формирование фильтров запроса БД.
    Пока сделано для формирования фильтров по
    типу `title__ilike`
    """
    queries = []
    for filter in filters:
        raw_filter_query, value = filter
        parse_operator(raw_filter_query, value, db_model)
    return queries
