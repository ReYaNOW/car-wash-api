from fastapi import APIRouter

from car_wash.cars.body_types.router import router as body_types_router
from car_wash.cars.brands.router import router as brands_router
from car_wash.cars.car_models.router import router as car_models_router
from car_wash.cars.configurations.router import router as configurations_router
from car_wash.cars.generations.router import router as generations_router

# Creating separate router to separate those routes from Cars tag
# in swagger doc

sub_router = APIRouter(
    prefix='/cars',
    tags=[
        'CarBrands, CarModels, CarGenerations, CarBodyTypes, CarConfiguration'
    ],
)

sub_router.include_router(brands_router)
sub_router.include_router(car_models_router)
sub_router.include_router(generations_router)
sub_router.include_router(body_types_router)
sub_router.include_router(configurations_router)
