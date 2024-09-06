from typing import Callable, ParamSpec

from fastapi import APIRouter, Depends

from car_wash.auth.dependencies import (
    get_user_admin,
    get_user_client,
    get_validate_access_to_entity,
)
from car_wash.utils.service import GenericCRUDService

CLIENT = 'Allowed to client or above'
OWNER = 'Allowed to owner or admin'
ADMIN = 'Allowed to admin only'

Param_init = ParamSpec('Param_init', bound=APIRouter.__init__)
Param_add_api_route = ParamSpec(
    'Param_add_api_route', bound=APIRouter.add_api_route
)


class CustomRouter(APIRouter):
    def __init__(
        self,
        *args: Param_init.args,
        default_description: str,
        **kwargs: Param_init.kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.default_description = default_description

    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        **kwargs: Param_add_api_route.kwargs,
    ) -> None:
        if not kwargs.get('description'):
            kwargs['description'] = self.default_description

        super().add_api_route(path, endpoint, **kwargs)


def get_client_router(prefix: str, tags: list[str]) -> CustomRouter:
    return CustomRouter(
        prefix=prefix,
        tags=tags,
        default_description=CLIENT,
        dependencies=[Depends(get_user_client)],
    )


def get_owner_router(
    prefix: str, service: type[GenericCRUDService], tags: list[str]
) -> CustomRouter:
    return CustomRouter(
        prefix=prefix,
        tags=tags,
        default_description=OWNER,
        dependencies=[Depends(get_validate_access_to_entity(service))],
    )


def get_admin_router(prefix: str, tags: list[str]) -> CustomRouter:
    return CustomRouter(
        prefix=prefix,
        tags=tags,
        default_description=ADMIN,
        dependencies=[Depends(get_user_admin)],
    )
