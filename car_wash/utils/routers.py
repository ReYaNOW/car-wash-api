from typing import Any, Callable

from fastapi import APIRouter, Depends

from car_wash.auth.dependencies import (
    get_user_admin,
    get_user_client,
    get_validate_access_to_entity,
)
from car_wash.utils.service import GenericCRUDService

CLIENT = 'Allowed to client or admin'
OWNER = 'Allowed to owner or admin'
ADMIN = 'Allowed to admin only'


class CustomRouter(APIRouter):
    def __init__(
        self,
        *args: Any,
        default_description: str,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.default_description = default_description

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        **kwargs: Any,
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
