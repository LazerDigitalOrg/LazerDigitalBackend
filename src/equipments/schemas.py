from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, field_validator


class EquipmentSchema(BaseModel):
    title: str
    description: Optional[str]
    characteristics: Optional[Union[dict, List[str]]]
    photo_url: Optional[str]

    @field_validator('characteristics')
    def validate_structure(cls, value: dict):
        if isinstance(value.get(0), list):
            return value.get(0)
        return value


class EquipmentCategorySchema(BaseModel):
    title: str
    equipment_slug: str
    photo_url: str


class EquipmentResponse(BaseModel):
    equipments: List[EquipmentCategorySchema]


class CategorySchema(BaseModel):
    title: str
    category_slug: str
    hint: str
    photo_url: str
    description: Optional[str]


class CategoryResponse(BaseModel):
    categories: List[CategorySchema]
