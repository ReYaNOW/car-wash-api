import asyncio
from collections import defaultdict
from datetime import datetime, timedelta

from fastapi import BackgroundTasks, UploadFile
from pydantic import HttpUrl

from car_wash.cars.body_types.repository import CarBodyTypeRepository
from car_wash.storage.schemas import S3Folders
from car_wash.storage.service import S3Service
from car_wash.storage.utils import validate_link
from car_wash.utils.schemas import GenericListResponse
from car_wash.utils.service import GenericCRUDService
from car_wash.washes.bookings.schemas import BookingCreate
from car_wash.washes.exceptions import (
    AlreadyActiveError,
    AlreadyNotActiveError,
    MissingRequiredBodyTypesError,
    NotEnoughScheduleRecordsError,
)
from car_wash.washes.models import Box, CarWash
from car_wash.washes.prices.repository import CarWashPriceRepository
from car_wash.washes.repository import CarWashRepository, RowProtocol
from car_wash.washes.schedules.repository import ScheduleRepository
from car_wash.washes.schemas import (
    CarWashCreate,
    CarWashList,
    CarWashRead,
    CarWashUpdate,
)

NUMBER_OF_DAYS_IN_WEEK = 7


class CarWashService(GenericCRUDService[CarWash]):
    repository = CarWashRepository
    crud_repo: CarWashRepository

    def __init__(self):
        super().__init__()
        self.s3_service = S3Service()
        self.schedule_repo = ScheduleRepository()
        self.body_type_repo = CarBodyTypeRepository()
        self.price_repo = CarWashPriceRepository()
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

        self.available_slots_by_box: dict[
            int, list[tuple[datetime, datetime]]
        ] = defaultdict(list)

        self._initialize_available_slots(date, rows)
        self._process_bookings()

        return self.available_slots_by_box

    def _initialize_available_slots(
        self, date: datetime.date, rows: list[RowProtocol]
    ) -> None:
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

    async def is_booking_possible(
        self, box: Box, new_booking: BookingCreate
    ) -> bool:
        available_times = await self.get_available_times(
            box.car_wash_id, new_booking.start_datetime.date()
        )
        if not available_times or box.id not in available_times:
            return False

        for datetime_range in available_times[box.id]:
            start_dt = datetime_range[0]
            end_dt = datetime_range[1]
            if (
                start_dt <= new_booking.start_datetime
                and end_dt >= new_booking.end_datetime
            ):
                return True

        return False

    async def create_car_wash(
        self,
        new_car_wash: CarWashCreate,
        image: UploadFile | None,
    ) -> int:
        if image:
            unique_filename = await self.s3_service.upload_file(
                S3Folders.CAR_WASHES, image
            )
            new_car_wash.image_path = unique_filename

        car_wash_id = await self.crud_repo.add_one(new_car_wash.model_dump())
        return car_wash_id

    async def read_car_wash(
        self,
        id_: int,
        bg_tasks: BackgroundTasks,
    ) -> CarWashRead:
        user = await self.crud_repo.find_one(id_)
        return await self.add_img_link_to_car_wash(user, bg_tasks)

    async def paginate_car_washes(
        self, query: CarWashList, bg_tasks: BackgroundTasks
    ) -> GenericListResponse:
        list_response = await self.paginate_entities(query)

        tasks = [
            self.add_img_link_to_car_wash(car_wash, bg_tasks)
            for car_wash in list_response.data
        ]

        res = await asyncio.gather(*tasks)
        list_response.data = res

        return list_response

    async def add_img_link_to_car_wash(
        self,
        car_wash: CarWash | CarWashRead,
        bg_tasks: BackgroundTasks,
    ) -> CarWashRead:
        if isinstance(car_wash, CarWash):
            car_wash = CarWashRead.model_validate(car_wash)

        img_link = car_wash.image_link

        if car_wash.image_path and (
            not img_link or not validate_link(img_link, car_wash.image_path)
        ):
            image_link = await self.s3_service.generate_link(
                car_wash.image_path
            )

            image_link = HttpUrl(image_link)
            car_wash.image_link = image_link
            new_img_link = f'{image_link.path}?{image_link.query}'

            bg_tasks.add_task(
                self.crud_repo.change_one,
                car_wash.id,
                {'image_link': new_img_link},
            )

        return car_wash

    async def update_car_wash(
        self,
        id: int,
        new_values: CarWashUpdate,
        img: UploadFile | None,
        bg_tasks: BackgroundTasks,
    ) -> CarWashRead:
        if img:
            car_wash = await self.read_entity(id)
            unique_filename = await self.s3_service.upload_file(
                S3Folders.CAR_WASHES, img, car_wash.image_path
            )

            new_values.image_path = unique_filename

        updated_car_wash = await self.update_entity(id, new_values)
        return await self.add_img_link_to_car_wash(updated_car_wash, bg_tasks)

    async def delete_car_wash(self, id: int) -> CarWash:
        car_wash = await self.crud_repo.delete_one(id)
        await self.s3_service.remove_file(car_wash.image_path)
        return car_wash

    async def show_car_wash(self, id: int) -> None:
        car_wash = await self.crud_repo.find_one(id)

        if car_wash.active is True:
            raise AlreadyActiveError

        records = await self.schedule_repo.count_records(
            filters=[self.schedule_repo.model.car_wash_id == id]
        )

        if records != NUMBER_OF_DAYS_IN_WEEK:
            raise NotEnoughScheduleRecordsError(records)

        necessary_bts = await self.body_type_repo.find_necessary_bts_ids()

        existing_body_types = set(
            await self.price_repo.select_body_types_from_price(id)
        )
        if not all(bt_id in existing_body_types for bt_id in necessary_bts):
            raise MissingRequiredBodyTypesError

        await self.crud_repo.change_one(id, {'active': True})

    async def hide_car_wash(self, id: int) -> None:
        car_wash = await self.crud_repo.find_one(id)

        if car_wash.active is True:
            raise AlreadyNotActiveError
        await self.crud_repo.change_one(id, {'active': False})
