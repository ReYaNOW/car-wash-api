class StartTimeGreaterError(ValueError):
    def __init__(self):
        super().__init__('start_time have to be lower then end_time')


class StartDatetimeGreaterError(ValueError):
    def __init__(self):
        super().__init__('start_datetime have to be lower then end_datetime')
