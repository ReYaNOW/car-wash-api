def validate_year_range(year_range: str) -> None:
    try:
        start_year, end_year = year_range.split('-', maxsplit=1)
        start_year: str | int
        end_year: str | int
    except ValueError:
        raise ValueError(
            'year_range should be in format. '
            "[start year | 'past']-[end year | 'present']"
        ) from None

    if not start_year.isnumeric() and start_year != 'past':
        raise ValueError("Start year have to be an year or equal to 'past'")

    if not end_year.isnumeric() and end_year != 'present':
        raise ValueError("End year have to be an year or equal to 'present'")

    if start_year.isnumeric():
        check_one_year_range(int(start_year))
    if end_year.isnumeric():
        check_one_year_range(int(end_year))


def check_one_year_range(value: int):
    if not 1886 <= value <= 2100:
        raise ValueError(
            'Both years have to be in range 1886-2100. '
            'End year have to be grater then start year'
        )
