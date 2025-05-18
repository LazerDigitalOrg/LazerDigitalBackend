from typing import List, Optional, Union

from pydantic import BaseModel, field_validator



class EquipmentSchema(BaseModel):
    title: str
    description: Optional[str]
    characteristics: Optional[Union[dict, List[str]]]
    photo_url: Optional[str]
    price: Optional[int]

    @field_validator('characteristics')
    def validate_structure(cls, value: dict):
        if isinstance(value.get(0), list):
            return value.get(0)
        return value


class EquipmentTitleSchema(BaseModel):
    title: str


class EventEquipmentCategorySchema(BaseModel):
    category_title: str
    equipments_catalog: List[EquipmentTitleSchema]


class EventEquipmentCategoryResponse(BaseModel):
    equipments_catalog: List[EventEquipmentCategorySchema]
    reed:str


class EquipmentCategorySchema(BaseModel):
    title: str
    equipment_slug: str
    photo_url: str
    price: Optional[int]


# {"equipmnets": [
#     {"Приборы скользящего света": [
#         {"quipment_id": 1, "title": "AXCOR BEAM"},
#         {"quipment_id": 2, "title": "AXCOR BEAM M6"}
# ]},
#     {"Световые пульты"[]}]}

# {"equipmnets": [
#         {"quantity": 1, "equipment_title": "AXCOR BEAM"},
#         {"quantity": 2, "equipment_title": "AXCOR BEAM M6"}
# ]},

class EquipmentResponse(BaseModel):
    title: str
    description: Optional[str]
    equipments: List[EquipmentCategorySchema]


class CategorySchema(BaseModel):
    title: str
    category_slug: str
    hint: str
    photo_url: str
    description: Optional[str]


class CategoryResponse(BaseModel):
    categories: List[CategorySchema]
