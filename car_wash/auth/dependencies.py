from typing import Annotated, TypeVar

from fastapi import Depends

from car_wash.auth.exceptions import (
    credentials_exc,
    inactive_user_exc,
    insufficient_permissions_exc,
    user_id_is_not_set_exc,
)
from car_wash.auth.schemas import oauth2_scheme
from car_wash.auth.service import AuthService
from car_wash.users.models import User
from car_wash.users.schemas import UserReadWithRole
from car_wash.utils.schemas import GenericListRequest
from car_wash.utils.service import GenericCRUDService


async def get_auth_service():
    return AuthService()


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)],
):
    token_data = service.process_token(token, token_type='access')
    user = await service.read_user_with_role(id=token_data.user_id)

    if user is None:
        raise credentials_exc

    return UserReadWithRole.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.active:
        raise inactive_user_exc
    return current_user


async def get_user_client(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    allowed_roles = {'client', 'admin'}

    if current_user.role.name not in allowed_roles:
        raise insufficient_permissions_exc
    return current_user


async def get_user_admin(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if current_user.role.name != 'admin':
        raise insufficient_permissions_exc
    return current_user


def get_validate_access_to_entity(service: type(GenericCRUDService)):
    async def validate_access_to_entity(
        id: int, current_user: Annotated[User, Depends(get_user_client)]
    ):
        entity = await service().read_entity(id)
        if hasattr(entity, 'user_id'):
            if entity.user_id != current_user.id:
                if current_user.role.name != 'admin':
                    raise insufficient_permissions_exc

        return entity

    return validate_access_to_entity


T = TypeVar('T', bound=GenericListRequest)


def get_validate_query_user_id(list_schema: type(T)):
    async def validate_query_user_id(
        query: Annotated[list_schema, Depends()],
        current_user: Annotated[User, Depends(get_user_client)],
    ):
        if hasattr(query, 'user_id'):
            if query.user_id != current_user.id:
                if current_user.role.name != 'admin':
                    raise user_id_is_not_set_exc

        return query

    return validate_query_user_id
