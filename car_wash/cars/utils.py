from car_wash.cars.exceptions import (
    InvalidEndYearError,
    InvalidStartYearError,
    InvalidYearRangeError,
    WrongFormatError,
)

MINIMAL_CAR_YEAR = 1886
MAX_CAR_YEAR = 2100


def validate_year_range(year_range: str) -> None:
    try:
        start_year, end_year = year_range.split('-', maxsplit=1)
        start_year: str | int
        end_year: str | int
    except ValueError:
        raise WrongFormatError from None

    if not start_year.isnumeric() and start_year != 'past':
        raise InvalidStartYearError

    if not end_year.isnumeric() and end_year != 'present':
        raise InvalidEndYearError

    if start_year.isnumeric():
        check_one_year_range(int(start_year))
    if end_year.isnumeric():
        check_one_year_range(int(end_year))


def check_one_year_range(value: int) -> None:
    if not MINIMAL_CAR_YEAR <= value <= MAX_CAR_YEAR:
        raise InvalidYearRangeError
