from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from car_wash.auth.router import router as auth_router
from car_wash.cars.router import router as cars_router
from car_wash.config import config
from car_wash.storage.service import S3Service
from car_wash.users.router import router as users_router
from car_wash.utils.custom_swagger_docs import (
    create_custom_swagger_docs,
    tags_metadata,
)
from car_wash.utils.data_migration.fill_db import add_default_users_and_roles
from car_wash.washes.router import router as car_washes_router
from car_wash.washes.router import sub_router as car_wash_locations_router


@asynccontextmanager
async def lifespan(_: Any) -> None:
    if config.debug:
        await add_default_users_and_roles()

        client = S3Service()
        await client.create_default_bucket()
    yield


app = FastAPI(
    docs_url=None,
    title='Car Wash',
    openapi_tags=tags_metadata,
    swagger_ui_parameters={'persistAuthorization': True},
    lifespan=lifespan,
)


create_custom_swagger_docs(app)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(car_wash_locations_router)
app.include_router(car_washes_router)
app.include_router(cars_router)
