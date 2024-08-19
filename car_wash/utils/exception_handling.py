from fastapi import HTTPException
from parse import compile
from sqlalchemy.exc import IntegrityError

NOT_PRESENT_PATTERN = compile(
    'Key ({field})=({input}) is not present in table'
)

ALREADY_EXISTS_PATTERN = compile('Key ({field})=({input}) already exists')

NOT_NULL_PATTERN = compile(
    'null value in column "{column_name}" violates not-null constraint'
)


def handle_integrity_error(e: IntegrityError, table_name: str):
    table_slug = table_name.capitalize().replace('_', ' ')
    original_driver_exception = str(e.orig)

    not_present = NOT_PRESENT_PATTERN.search(original_driver_exception)
    if not_present:
        field, input_ = get_values(not_present, 'field', 'input')
        specific_table_name, field = field.rsplit('_', maxsplit=1)
        raise HTTPException(
            status_code=409,
            detail=f'{specific_table_name} with '
            f'{field}={input_} is not exists',
        ) from None

    already_exists = ALREADY_EXISTS_PATTERN.search(original_driver_exception)
    if already_exists:
        field, input_ = get_values(already_exists, 'field', 'input')
        raise HTTPException(
            status_code=409,
            detail=f'{table_slug} with {field}={input_} already exists',
        ) from None

    not_null = NOT_NULL_PATTERN.search(original_driver_exception)
    if not_null:
        column_name = get_values(not_null, 'column_name')[0]
        msg = f'Field {column_name} is required'.replace('"', '')
        raise HTTPException(status_code=409, detail=msg)

    raise HTTPException(status_code=500) from e


def get_values(result, *args):
    new_values = []
    for value in args:
        try:
            new_values.append(result[value])
        except KeyError:
            new_values.append(None)

    return new_values
