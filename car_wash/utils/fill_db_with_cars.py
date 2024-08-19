import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from car_wash.cars.models import (
    CarBodyType,
    CarBrand,
    CarConfiguration,
    CarGeneration,
    CarModel,
)
from car_wash.config import config

DATABASE_URL = config.database_url.unicode_string()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


#
# pprint(data[43]['models'][0]['generations'][0]['configurations'])


# Обработка данных и добавление в базу данных
def fill_db():
    with open('base.json', encoding='UTF-8') as file:
        data = json.load(file)

    counter = 0
    for brand_data in data:
        counter += 1
        if counter % 15 == 0:
            print(counter)

        brand_name = brand_data['name']
        brand = session.query(CarBrand).filter_by(name=brand_name).first()
        if not brand:
            brand = CarBrand(name=brand_name)
            session.add(brand)
            session.commit()
        else:
            pass
            # print(f"Бренд '{brand_name}' уже существует в базе данных.")

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
            else:
                pass
                # print(f"Модель '{model_name}' уже существует в базе данных.")

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
                else:
                    pass
                    # print(
                    #     f"Поколение '{generation_name}'
                    #     уже существует в базе данных."
                    # )

                for configuration_data in generation_data['configurations']:
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
                    else:
                        pass
                        # print(
                        #     f"Тип кузова '{body_type_name}'
                        #     уже существует в базе данных."
                        # )

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
                    else:
                        pass
                        # print(
                        #     f"Конфигурация с поколением '{generation_name}'
                        #     и кузовом '{body_type_name}'
                        #     уже существует в базе данных."
                        # )
    config.filling_db = False
    print('Данные успешно обработаны.')
