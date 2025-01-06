from car_wash.cars.body_types.repository import CarBodyTypeRepository
from car_wash.cars.configurations.repository import CarConfigurationRepository
from car_wash.cars.repository import UserCarRepository
from car_wash.utils.service import GenericCRUDService
from car_wash.washes.bookings.repository import BookingRepository
from car_wash.washes.bookings.schemas import BookingCreate
from car_wash.washes.boxes.repository import BoxRepository
from car_wash.washes.exceptions import BookingIsNotAvailableError
from car_wash.washes.models import Booking
from car_wash.washes.prices.repository import CarWashPriceRepository
from car_wash.washes.service import CarWashService


class BookingService(GenericCRUDService[Booking]):
    repository = BookingRepository

    def __init__(self):
        super().__init__()
        self.car_wash_service = CarWashService()
        self.box_repo = BoxRepository()
        self.price_repo = CarWashPriceRepository()
        self.user_car_repo = UserCarRepository()
        self.car_config_repo = CarConfigurationRepository()
        self.car_body_type_repo = CarBodyTypeRepository()

    async def create_booking(self, new_booking: BookingCreate) -> int:
        box = await self.box_repo.find_one(new_booking.box_id)

        if not await self.car_wash_service.is_booking_possible(
            box, new_booking
        ):
            raise BookingIsNotAvailableError

        user_car = await self.user_car_repo.find_one(new_booking.user_car_id)
        car_config = await self.car_config_repo.find_one(
            user_car.configuration_id
        )

        price_model = self.price_repo.model
        self.price_repo.raise_404_when_find_one_not_found = False
        price_entity = await self.price_repo.find_one_by_custom_fields(
            [
                price_model.car_wash_id == box.car_wash_id,
                price_model.body_type_id == car_config.body_type_id,
            ]
        )
        self.price_repo.raise_404_when_find_one_not_found = True
        if not price_entity:
            body_type = await self.car_body_type_repo.find_one(
                car_config.body_type_id
            )

            price_entity = await self.price_repo.find_one_by_custom_fields(
                [
                    price_model.car_wash_id == box.car_wash_id,
                    price_model.body_type_id == body_type.parent_id,
                ]
            )

        new_booking.price = price_entity.price

        entity_dict = new_booking.model_dump()
        entity_id = await self.crud_repo.add_one(entity_dict)
        return entity_id
