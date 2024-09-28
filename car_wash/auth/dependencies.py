from typing import Annotated, Any, Callable, Coroutine

from fastapi import Depends

from car_wash.auth.exceptions import (
    CredentialsExc,
    InactiveUserExc,
    InsufficientPermissionsExc,
    UserIdIsNotSetExc,
)
from car_wash.auth.schemas import oauth2_scheme
from car_wash.auth.utils import AnnTokenService, TokenType
from car_wash.users.models import User
from car_wash.users.schemas import UserReadWithRole
from car_wash.users.service import AnnUserService
from car_wash.utils.repository import AnyModel
from car_wash.utils.schemas import GenericListRequest
from car_wash.utils.service import GenericCRUDService


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: AnnTokenService,
    user_service: AnnUserService,
) -> UserReadWithRole:
    user_id = token_service.process_token(token, TokenType.ACCESS)
    user = await user_service.read_user_with_role(id=user_id)

    if user is None:
        raise CredentialsExc

    return UserReadWithRole.model_validate(user)


async def get_current_active_user(
    current_user: Annotated[UserReadWithRole, Depends(get_current_user)],
) -> UserReadWithRole:
    if not current_user.active:
        raise InactiveUserExc
    return current_user


async def get_user_client(
    current_user: Annotated[
        UserReadWithRole, Depends(get_current_active_user)
    ],
) -> UserReadWithRole:
    allowed_roles = {'client', 'admin'}

    if current_user.role.name not in allowed_roles:
        raise InsufficientPermissionsExc
    return current_user


async def get_user_admin(
    current_user: Annotated[
        UserReadWithRole, Depends(get_current_active_user)
    ],
) -> UserReadWithRole:
    if current_user.role.name != 'admin':
        raise InsufficientPermissionsExc
    return current_user


def get_validate_access_to_entity(
    service: type[GenericCRUDService],
) -> Callable[[int, UserReadWithRole], Coroutine[Any, Any, AnyModel]]:
    async def validate_access_to_entity(
        id: int,
        current_user: Annotated[UserReadWithRole, Depends(get_user_client)],
    ) -> AnyModel:
        entity = await service().read_entity(id)
        check_user_id(entity, current_user)

        return entity

    return validate_access_to_entity


def get_validate_query_user_id(
    list_schema: type[GenericListRequest],
) -> Callable[
    [GenericListRequest, UserReadWithRole],
    Coroutine[Any, Any, GenericListRequest],
]:
    async def validate_query_user_id(
        query: Annotated[list_schema, Depends()],
        current_user: Annotated[UserReadWithRole, Depends(get_user_client)],
    ) -> list_schema:
        check_user_id(query, current_user)
        return query

    return validate_query_user_id


def check_user_id(
    value: GenericListRequest | AnyModel, current_user: UserReadWithRole
) -> None:
    if (
        (
            hasattr(value, 'user_id')
            and value.user_id != current_user.id
            and current_user.role.name != 'admin'
        )
        or isinstance(value, User)
        and current_user.id != value.id
        and current_user.role.name != 'admin'
    ):
        raise UserIdIsNotSetExc
