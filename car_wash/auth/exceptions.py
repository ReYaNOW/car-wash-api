from fastapi import HTTPException, status

InactiveUserExc = HTTPException(status_code=400, detail='Inactive user')

InsufficientPermissionsExc = HTTPException(
    status_code=403, detail='Insufficient permissions'
)

UserIdIsNotSetExc = HTTPException(
    status_code=400, detail='user_id have to be equal to authenticated user'
)


default_fields = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'headers': {'WWW-Authenticate': 'Bearer'},
}

ExpiredTokenExc = HTTPException(**default_fields, detail='Token has expired')

CredentialsExc = HTTPException(
    **default_fields, detail='Could not validate credentials'
)

InvalidTokenTypeExc = HTTPException(
    **default_fields, detail='Invalid token type'
)

RefreshTokenIsUsedExc = HTTPException(
    **default_fields, detail='Refresh token already used'
)


class MissingCredentialsError(ValueError):
    def __init__(self):
        super().__init__('id or both username and password is required')
