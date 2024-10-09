from fastapi import HTTPException


class StartTimeGreaterError(ValueError):
    def __init__(self):
        super().__init__('start_time have to be lower then end_time')


class StartDatetimeGreaterError(ValueError):
    def __init__(self):
        super().__init__('start_datetime have to be lower then end_datetime')


class NotTwoHoursError(ValueError):
    def __init__(self):
        super().__init__(
            'range between end_datetime and start_datetime should '
            'equal to 2 hours'
        )


class NotEnoughScheduleRecordsError(HTTPException):
    def __init__(self, number: int | str):
        super().__init__(
            status_code=400,
            detail=f'There should be 7 records for schedule per car wash, '
            f'found: {number}',
        )


class MissingRequiredBodyTypesError(HTTPException):
    def __init__(self, missing_body_types: list[int]):
        detail = {
            'detail': 'There are missing prices for some required '
            'car body types.',
            'missing_body_type_ids': missing_body_types,
        }
        super().__init__(status_code=400, detail=detail)


class AlreadyActiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail='This car wash already showing'
        )


class AlreadyNotActiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400, detail='This car wash already hidden'
        )


class BookingIsNotAvailableError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail='Booking for these start_datetime and end_datetime '
            'is not available',
        )
