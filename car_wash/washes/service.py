from collections import defaultdict
from datetime import datetime, timedelta

from car_wash.utils.service import GenericCRUDService
from car_wash.washes.models import CarWash
from car_wash.washes.repository import CarWashRepository, RowProtocol


class CarWashService(GenericCRUDService[CarWash]):
    repository = CarWashRepository
    crud_repo: CarWashRepository

    def __init__(self):
        super().__init__()
        self.available_slots_by_box = None
        self.schedule_end_by_box = None
        self.last_end_time_by_box = None

        self.min_duration = timedelta(hours=2)

    async def get_available_times(
        self, car_wash_id: int, date: datetime.date
    ) -> dict[int, list[tuple[datetime, datetime]]]:
        rows: list[
            RowProtocol
        ] = await self.crud_repo.fetch_schedule_and_booking(car_wash_id, date)

        if not rows:
            return {}

        self._initialize_available_slots(date, rows)
        self._process_bookings()

        return dict(self.available_slots_by_box)

    def _initialize_available_slots(
        self, date: datetime.date, rows: list[RowProtocol]
    ) -> None:
        self.available_slots_by_box: dict[
            int, list[tuple[datetime, datetime]]
        ] = defaultdict(list)

        # Track the last end time for each box to calculate the next
        # available slot
        self.last_end_time_by_box = {}
        self.schedule_end_by_box = {}

        for row in rows:
            box_id = row.box_id
            schedule_start = datetime.combine(date, row.start_time)
            schedule_end = datetime.combine(date, row.end_time)

            # Store the schedule_end for this box
            if box_id not in self.last_end_time_by_box:
                self.last_end_time_by_box[box_id] = schedule_start
                self.schedule_end_by_box[box_id] = schedule_end

            # Determine the starting point for available slots
            previous_booking_end = self.last_end_time_by_box[box_id]

            # If there are no bookings for this box, the entire schedule is
            # available
            if row.start_datetime is None:
                self.available_slots_by_box[box_id].append(
                    (schedule_start, schedule_end)
                )
            else:
                # Calculate available slot before the current booking
                if row.start_datetime > previous_booking_end:
                    new_start = previous_booking_end
                    new_end = row.start_datetime

                    # Merge if they overlap or are adjacent
                    if (
                        self.available_slots_by_box[box_id]
                        and self.available_slots_by_box[box_id][-1][1]
                        >= new_start
                    ):
                        # Merge with the last slot
                        last_start, last_end = self.available_slots_by_box[
                            box_id
                        ].pop()
                        self.available_slots_by_box[box_id].append(
                            (last_start, max(last_end, new_end))
                        )
                    elif new_end - new_start >= self.min_duration:
                        self.available_slots_by_box[box_id].append(
                            (new_start, new_end)
                        )

                # Update the last booking end time to the current
                # booking's end time
                self.last_end_time_by_box[box_id] = max(
                    previous_booking_end, row.end_datetime
                )

    def _process_bookings(self) -> None:
        for box_id, last_end_time in self.last_end_time_by_box.items():
            schedule_end = self.schedule_end_by_box[box_id]
            if last_end_time < schedule_end:
                new_start = last_end_time
                new_end = schedule_end

                # Merge if they overlap or are adjacent
                if (
                    self.available_slots_by_box[box_id]
                    and self.available_slots_by_box[box_id][-1][1] >= new_start
                ):
                    # Merge with the last slot
                    last_start, last_end = self.available_slots_by_box[
                        box_id
                    ].pop()
                    self.available_slots_by_box[box_id].append(
                        (last_start, max(last_end, new_end))
                    )
                elif new_end - new_start >= self.min_duration:
                    self.available_slots_by_box[box_id].append(
                        (new_start, new_end)
                    )
