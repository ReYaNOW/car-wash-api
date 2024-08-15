from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.brands import schemas
from car_wash.cars.brands.service import CarBrandService

router = APIRouter(prefix='/brands')


@router.post('', response_model=schemas.CreateResponse)
async def create_brand(new_brand: schemas.BrandCreate):
    brand_id = await CarBrandService().create_entity(new_brand)
    return {'brand_id': brand_id}


@router.get('/{id}', response_model=schemas.ReadResponse)
async def read_brand(id: int):
    brand = await CarBrandService().read_entity(id)
    return brand


@router.get('', response_model=list[schemas.ReadResponse])
async def list_brands(query: Annotated[schemas.BrandList, Depends()]):
    brands = await CarBrandService().list_entities(query)
    return brands


@router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    description='Update certain fields of existing brand',
)
async def update_brand(id: int, new_values: schemas.BrandUpdate):
    updated_brand = await CarBrandService().update_entity(id, new_values)
    return updated_brand


@router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_brand(id: int):
    id_ = await CarBrandService().delete_entity(id)
    return {'detail': f'Brand successfully deleted with id: {id_}'}
