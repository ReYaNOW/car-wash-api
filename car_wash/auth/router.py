from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from car_wash.auth.schemas import Tokens, oauth2_scheme
from car_wash.auth.service import AnnAuthService
from car_wash.storage.schemas import AnnValidateImage
from car_wash.users.schemas import UserRegistration

router = APIRouter(prefix='/jwt', tags=['JWT'])


@router.post('/register')
async def register(
    new_user: UserRegistration,
    service: AnnAuthService,
    img: AnnValidateImage,
) -> Tokens:
    tokens = await service.register(new_user, img)
    return tokens


@router.post('/token')
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AnnAuthService,
) -> Tokens:
    tokens = await service.login(form_data.username, form_data.password)
    return tokens


@router.post('/refresh')
async def refresh(
    refresh_token: Annotated[str, Depends(oauth2_scheme)],
    service: AnnAuthService,
) -> Tokens:
    tokens = await service.refresh_tokens(refresh_token)
    return tokens
