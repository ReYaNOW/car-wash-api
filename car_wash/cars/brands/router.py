from typing import Annotated

from fastapi import APIRouter, Depends

from car_wash.cars.brands import schemas
from car_wash.cars.brands.service import CarBrandService
from car_wash.utils.router import get_admin_router, get_client_router

router = APIRouter()

client_router = get_client_router('/brands')
admin_router = get_admin_router('/brands')


@admin_router.post('', response_model=schemas.CreateResponse)
async def create_brand(new_brand: schemas.BrandCreate):
    brand_id = await CarBrandService().create_entity(new_brand)
    return {'brand_id': brand_id}


@client_router.get('/{id}', response_model=schemas.ReadResponse)
async def read_brand(id: int):
    brand = await CarBrandService().read_entity(id)
    return brand


@client_router.get('', response_model=schemas.ListResponse)
async def list_brands(query: Annotated[schemas.BrandList, Depends()]):
    paginated_brands = await CarBrandService().paginate_entities(query)
    return paginated_brands


@admin_router.patch(
    '/{id}',
    response_model=schemas.UpdateResponse,
    summary='Update certain fields of existing brand',
)
async def update_brand(id: int, new_values: schemas.BrandUpdate):
    updated_brand = await CarBrandService().update_entity(id, new_values)
    return updated_brand


@admin_router.delete('/{id}', response_model=schemas.DeleteResponse)
async def delete_brand(id: int):
    id_ = await CarBrandService().delete_entity(id)
    return {'detail': f'Brand successfully deleted with id: {id_}'}


router.include_router(client_router)
router.include_router(admin_router)
