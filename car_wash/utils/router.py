from typing import Callable

from fastapi import APIRouter, Depends

from car_wash.auth.dependencies import (
    get_user_admin,
    get_user_client,
    get_validate_access_to_entity,
)

CLIENT = 'Allowed to client or above'
OWNER = 'Allowed to owner or admin'
ADMIN = 'Allowed to admin only'


class CustomRouter(APIRouter):
    def __init__(self, *args, default_description: str, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_description = default_description

    def add_api_route(self, path: str, endpoint: Callable, **kwargs):
        if not kwargs.get('description'):
            kwargs['description'] = self.default_description

        super().add_api_route(path, endpoint, **kwargs)


def get_client_router(prefix: str):
    return CustomRouter(
        prefix=prefix,
        default_description=CLIENT,
        dependencies=[Depends(get_user_client)],
    )


def get_owner_router(prefix: str, service):
    return CustomRouter(
        prefix=prefix,
        default_description=OWNER,
        dependencies=[Depends(get_validate_access_to_entity(service))],
    )


def get_admin_router(prefix: str):
    return CustomRouter(
        prefix=prefix,
        default_description=ADMIN,
        dependencies=[Depends(get_user_admin)],
    )
