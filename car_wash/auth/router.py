from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from car_wash.auth.dependencies import get_auth_service
from car_wash.auth.schemas import Tokens, oauth2_scheme
from car_wash.auth.service import AuthService
from car_wash.users.schemas import UserRegistration

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.post('/register')
async def register(
    new_user: UserRegistration,
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Tokens:
    tokens = await service.register(new_user)
    return tokens


@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Tokens:
    tokens = await service.login(form_data.username, form_data.password)
    return tokens


@router.post('/refresh')
async def refresh(
    refresh_token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> Tokens:
    tokens = await service.refresh_tokens(refresh_token)
    return tokens