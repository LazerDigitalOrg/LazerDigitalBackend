from datetime import datetime
from typing import List,Optional

from pydantic import BaseModel


class EquipmentSchema(BaseModel):
    title: str
    description: str
    power: Optional[str]
    total_power: Optional[str]
    producer: str
    characteristics: dict
    weight: int
    photo_url: Optional[str]

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
    description: str



class CategoryResponse(BaseModel):
    categories: List[CategorySchema]
