from fastapi import HTTPException, status

inactive_user_exc = HTTPException(status_code=400, detail='Inactive user')

insufficient_permissions_exc = HTTPException(
    status_code=403, detail='Insufficient permissions'
)

user_id_is_not_set_exc = HTTPException(
    status_code=400, detail='user_id have to be equal to authenticated user'
)


default_fields = {
    'status_code': status.HTTP_401_UNAUTHORIZED,
    'headers': {'WWW-Authenticate': 'Bearer'},
}

expired_token_exc = HTTPException(**default_fields, detail='Token has expired')

credentials_exc = HTTPException(
    **default_fields, detail='Could not validate credentials'
)

invalid_token_type_exc = HTTPException(
    **default_fields, detail='Invalid token type'
)

refresh_token_is_used_exc = HTTPException(
    **default_fields, detail='Refresh token already used'
)
