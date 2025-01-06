import csv
import json

from sqlalchemy import create_engine, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker, Session

from car_wash.auth.utils import PasswordService
from car_wash.cars.models import (
    CarBodyType,
    CarBrand,
    CarConfiguration,
    CarGeneration,
    CarModel,
)
from car_wash.config import config
from car_wash.database import async_session_maker
from car_wash.users.models import Role, User

DATABASE_URL = config.database_url.unicode_string()
engine = create_engine(DATABASE_URL)
session_maker = sessionmaker(bind=engine)


def fill_db_cars():
    print('до')
    with open(
        'car_wash/utils/data_migration/data_sets/cars.json', encoding='UTF-8'
    ) as file:
        data = json.load(file)
    print('после')

    with session_maker() as session:
        print('начал')
        counter = 0
        for brand_data in data:
            counter += 1
            print(counter)
            if counter % 15 == 0:
                print(counter)

            brand_name = brand_data['name']
            brand = session.query(CarBrand).filter_by(name=brand_name).first()
            if not brand:
                brand = CarBrand(name=brand_name)
                session.add(brand)
                session.commit()

            for model_data in brand_data['models']:
                # Создание или получение записи CarModel
                model_name = model_data['name']
                model = (
                    session.query(CarModel)
                    .filter_by(name=model_name, brand_id=brand.id)
                    .first()
                )
                if not model:
                    model = CarModel(name=model_name, brand_id=brand.id)
                    session.add(model)
                    session.commit()

                for generation_data in model_data['generations']:
                    # Создание или получение записи CarGeneration
                    generation_name = generation_data['name']
                    start_year = generation_data['year-start']
                    end_year = generation_data['year-stop']

                    if start_year is None:
                        start_year = 'past'
                    if end_year is None:
                        end_year = 'present'

                    generation = (
                        session.query(CarGeneration)
                        .filter_by(name=generation_name, model_id=model.id)
                        .first()
                    )
                    if not generation:
                        generation = CarGeneration(
                            name=generation_name,
                            model_id=model.id,
                            start_year=start_year,
                            end_year=end_year,
                        )
                        session.add(generation)
                        session.commit()

                    for configuration_data in generation_data[
                        'configurations'
                    ]:
                        # Создание или получение записи CarBodyType
                        body_type_name = configuration_data['body-type']
                        body_type = (
                            session.query(CarBodyType)
                            .filter_by(name=body_type_name)
                            .first()
                        )
                        if not body_type:
                            body_type = CarBodyType(name=body_type_name)
                            session.add(body_type)
                            session.commit()

                        # Создание записи CarConfiguration
                        configuration = (
                            session.query(CarConfiguration)
                            .filter_by(
                                generation_id=generation.id,
                                body_type_id=body_type.id,
                            )
                            .first()
                        )
                        if not configuration:
                            configuration = CarConfiguration(
                                generation_id=generation.id,
                                body_type_id=body_type.id,
                            )
                            session.add(configuration)
                            session.commit()

    config.filling_db = False
    print('Данные успешно обработаны.')


token_service = PasswordService()
get_pass_hash = token_service.get_pass_hash


async def add_default_users_and_roles():
    async with async_session_maker() as session:
        admin_role = await session.execute(
            select(Role).filter_by(name='admin')
        )
        client_role = await session.execute(
            select(Role).filter_by(name='client')
        )

        if not admin_role.scalars().first():
            admin_role = Role(name='admin')
            session.add(admin_role)

        if not client_role.scalars().first():
            client_role = Role(name='client')
            session.add(client_role)

        await session.commit()

        admin_user = await session.execute(
            select(User).filter_by(username=config.admin_username)
        )
        client_user = await session.execute(
            select(User).filter_by(username='client')
        )

        if not admin_user.scalars().first():
            admin_role_result = await session.execute(
                select(Role).filter_by(name='admin')
            )
            admin_role = admin_role_result.scalars().first()

            hashed_pass = get_pass_hash(config.admin_password)
            admin_user = User(
                username=config.admin_username,
                hashed_password=hashed_pass,
                first_name='Admin',
                last_name='User',
                confirmed=True,
                active=True,
                role_id=admin_role.id,
            )
            session.add(admin_user)

        if not client_user.scalars().first():
            client_role_result = await session.execute(
                select(Role).filter_by(name='client')
            )
            client_role = client_role_result.scalars().first()

            hashed_pass = get_pass_hash('user_pass')
            client_user = User(
                username='client',
                hashed_password=hashed_pass,
                first_name='Client',
                last_name='User',
                confirmed=True,
                active=True,
                role_id=client_role.id,
            )
            session.add(client_user)

        await session.commit()


def read_csv():
    car_body_data = []
    with open(
        'car_wash/utils/data_migration/data_sets/car_body_types.csv',
        newline='',
        encoding='utf-8',
    ) as csvfile:
        reader = csv.DictReader(csvfile)
        row: dict
        for row in reader:
            car_body_data.append(
                {
                    "name": row['name'],
                    "parent_name": row['parent_name']
                    if row['parent_name'] != 'None'
                    else None,
                }
            )
    return car_body_data


def upsert_car_body_types(session: Session, data):
    # Сначала добавляем кузова без родительских элементов
    for row in data:
        if row['parent_name'] is None or row['parent_name'] == 'None':
            # Добавляем кузова без родителей
            values = {
                "name": row['name'],
                "parent_id": None,
            }
            stmt = insert(CarBodyType).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=['name'],
                set_=values,
            )
            session.execute(stmt)

    # Теперь добавляем кузова с родительскими элементами
    for row in data:
        if row['parent_name'] and row['parent_name'] != 'None':
            parent = session.scalar(
                select(CarBodyType.id).where(
                    CarBodyType.name == row['parent_name']
                )
            )

            values = {
                "name": row['name'],
                "parent_id": parent if parent is not None else None,
            }
            stmt = insert(CarBodyType).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=['name'],
                set_=values,
            )
            session.execute(stmt)

    session.commit()


async def update_db_with_body_types():
    data = read_csv()
    with session_maker() as session:
        upsert_car_body_types(session, data)
    config.filling_db = False
    print('car__body_type успешно обновлены')
