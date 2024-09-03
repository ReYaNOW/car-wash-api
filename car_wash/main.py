from fastapi import FastAPI

from car_wash.auth.router import router as auth_router
from car_wash.cars.router import router as cars_router
from car_wash.cars.sub_router import sub_router as sub_cars_router
from car_wash.users.router import router as users_router
from car_wash.washes.router import router as car_washes_router
from car_wash.washes.router import sub_router as car_wash_locations_router

tags_metadata = [
    {
        'name': 'JWT',
        'description': 'Operations with **jwt tokens** and **users**.',
    },
    {
        'name': 'Users',
        'description': 'Operations with **users**.',
    },
    {
        'name': 'CarWashes',
        'description': 'Operations with **Car Washes**',
    },
    {
        'name': 'CarWashLocations',
        'description': 'Operations with **Car Wash Locations**',
    },
    {
        'name': 'Cars',
        'description': 'Operations with **cars**.',
    },
    {
        'name': 'CarBrands, CarModels, CarGenerations, '
        'CarBodyTypes, CarConfiguration',
        'description': 'Operations with  **Car** **attributes**',
    },
]


app = FastAPI(
    title='Car Wash',
    openapi_tags=tags_metadata,
    swagger_ui_parameters={'persistAuthorization': True},
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(car_wash_locations_router)
app.include_router(car_washes_router)
app.include_router(sub_cars_router)
app.include_router(cars_router)
