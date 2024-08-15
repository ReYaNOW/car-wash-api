from fastapi import FastAPI

from car_wash.cars.router import router as cars_router
from car_wash.cars.router import sub_router as sub_cars_router
from car_wash.users.router import router as users_router

tags_metadata = [
    {
        'name': 'Users',
        'description': 'Operations with **users**.',
    },
    {
        'name': 'Cars',
        'description': 'Operations with **cars**.',
    },
    {
        'name': 'CarBodyType, CarBrands, CarGenerations',
        'description': 'Operations with  **Car** **attributes**',
    },
]


app = FastAPI(title='Car Wash', openapi_tags=tags_metadata)

app.include_router(sub_cars_router)
app.include_router(cars_router)
app.include_router(users_router)
