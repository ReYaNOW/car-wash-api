from fastapi import FastAPI

from car_wash.auth.router import router as auth_router
from car_wash.cars.router import router as cars_router
from car_wash.users.router import router as users_router
from car_wash.utils.custom_swagger_docs import (
    create_custom_swagger_docs,
    tags_metadata,
)
from car_wash.washes.router import router as car_washes_router
from car_wash.washes.router import sub_router as car_wash_locations_router

app = FastAPI(
    docs_url=None,
    title='Car Wash',
    openapi_tags=tags_metadata,
    swagger_ui_parameters={'persistAuthorization': True},
)


create_custom_swagger_docs(app)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(car_wash_locations_router)
app.include_router(car_washes_router)
app.include_router(cars_router)
