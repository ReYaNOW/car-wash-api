from enum import Enum
from typing import Annotated, Any

from fastapi import Depends, UploadFile
from pydantic import BaseModel, model_validator

from car_wash.storage.dependencies import validate_img


class CustomBaseModel(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value: str | Any) -> 'CustomBaseModel | str':
        if isinstance(value, str):
            return cls.model_validate_json(value)
        return value


class S3Folders(Enum):
    AVATARS = 'avatars'
    CAR_WASHES = 'car_washes'


AnnValidateImage = Annotated[UploadFile | None, Depends(validate_img)]
