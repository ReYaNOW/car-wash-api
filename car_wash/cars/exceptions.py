class WrongFormatError(ValueError):
    def __init__(self):
        super().__init__(
            'year_range should be in format. '
            "[start year | 'past']-[end year | 'present']"
        )


class InvalidStartYearError(ValueError):
    def __init__(self):
        super().__init__("Start year have to be an year or equal to 'past'")


class InvalidEndYearError(ValueError):
    def __init__(self):
        super().__init__("End year have to be an year or equal to 'present'")


class InvalidYearRangeError(ValueError):
    def __init__(self, start_year: int | str, end_year: int | str):
        super().__init__(
            f'Both years have to be in range {start_year}-{end_year}. '
            'End year have to be grater then start year'
        )
