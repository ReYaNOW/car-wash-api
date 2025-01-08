import functools
import inspect
from typing import TYPE_CHECKING, Any, Callable

from fastapi import HTTPException
from parse import Result, compile
from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from car_wash.utils.repository import SQLAlchemyRepository

NOT_PRESENT_PATTERN = compile(
    'Key ({field})=({input}) is not present in table'
)

ALREADY_EXISTS_PATTERN = compile('Key ({field})=({input}) already exists')

NOT_NULL_PATTERN = compile(
    'null value in column "{column_name}" violates not-null constraint'
)


def handle_integrity_error(e: IntegrityError, table_name: str) -> None:
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


def get_values(result: Result, *args: str) -> list[str]:
    new_values = []
    try:
        for value in args:
            new_values.append(result[value])
    except KeyError:
        new_values.append(None)
    return new_values


def orm_errors_handler(
    func: Callable[..., Any],
) -> Callable[..., Any]:
    @functools.wraps(func)
    async def wrapper(
        self: 'SQLAlchemyRepository', *args: Any, **kwargs: Any
    ) -> Any:
        try:
            result = await func(self, *args, **kwargs)
            if result is None and self.raise_404_when_find_one_not_found:
                func_name = func.__name__

                # Use inspect to get the argument names of the function
                signature = inspect.signature(func)
                param_names = list(signature.parameters.keys())[1:]

                # Create a dictionary of argument names and values
                args_dict = {param_names[i]: args[i] for i in range(len(args))}
                args_str = ', '.join(
                    f'{key}={value}' for key, value in args_dict.items()
                )

                kwargs_str = ', '.join(
                    f'{key}={value}' for key, value in kwargs.items()
                )

                details = (
                    f'Function: {func_name}, '
                    f'Args: ({args_str}), Kwargs: ({kwargs_str})'
                )
                raise HTTPException(
                    status_code=404, detail=f'{self.model}, {details}'
                )
        except IntegrityError as e:
            handle_integrity_error(e, self.model.__tablename__)
        else:
            return result

    return wrapper
