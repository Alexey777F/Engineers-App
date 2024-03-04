from sqlalchemy import create_engine, MetaData, Integer, String, Column, Date, Table, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from typing import Dict, List
from datetime import datetime, timedelta
import os
from logger_conf import Logger

logger = Logger()
url = f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER')}:" \
                                                     f"{os.environ.get('POSTGRES_PASSWORD')}@" \
                                                     f"{os.environ.get('PG_DB_HOST')}:5432/" \
                                                     f"{os.environ.get('PG_DB_NAME')}"
engine = create_engine(url=url, echo=False, pool_size=5, max_overflow=10)
metadata = MetaData()
Base = declarative_base()
sessionfactory = sessionmaker(bind=engine)


engineer_direction = Table('engineer_direction', Base.metadata,
    Column('engineer_id', Integer, ForeignKey('engineer.id')),
    Column('direction_id', Integer, ForeignKey('direction.id'))
)


class Engineer(Base):
    __tablename__ = 'engineer'
    id = Column(Integer(), primary_key=True)
    username = Column(String(12), nullable=False)
    password = Column(String(255), nullable=False)
    last_name = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    patronymic = Column(String(100), nullable=False)
    working_position = Column(String(70), nullable=False)
    city = Column(String(30), nullable=False)
    phone_number = Column(String(11), nullable=False)
    email = Column(String(50), nullable=False)
    created_on = Column(Date())
    direction = relationship('Direction', secondary='engineer_direction')
    tasks = relationship('Task', backref='assigned_engineer', cascade='all, delete-orphan')
    vacations = relationship('Vacation', cascade='all, delete-orphan')

    @classmethod
    def add_engineer(cls, username, password, last_name, name, patronymic, working_position, city, phone_number, email,
                     created_on):
        """Метод класса который добавляет инженера в базу"""
        engineer = cls(username=username, password=password, last_name=last_name, name=name, patronymic=patronymic,
                       working_position=working_position, city=city, phone_number=phone_number, email=email,
                       created_on=created_on)
        with sessionfactory() as session:
            session.add(engineer)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Ошибка {e} при добавлении данных в таблицу Engineer(Инженеры)")
                session.rollback()

    @classmethod
    def add_engineer_directions(cls, username: str, last_name: str, choice_directions: List):
        """Метод класса который добавляет связи направлений деятельности с инженером"""
        with sessionfactory() as session:
            engineers_data = {f'{last_name}': choice_directions}
            for last_na, networks in engineers_data.items():
                engineer = session.query(cls).filter(cls.username == username).first()
                if engineer:
                    for network in networks:
                        direction = session.query(Direction).filter(Direction.name == network).first()
                        if direction:
                            engineer.direction.append(direction)
                        else:
                            logger.error(f"Направление '{network}' не найдено в базе данных.")
                else:
                    return None
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Ошибка {e} при добавлении данных в таблицу engineer_directions")
                session.rollback()

    @classmethod
    def get_id_by_username(cls, username: str):
        """Метод класса который возвращает айди инженера по переданному username"""
        with sessionfactory() as session:
            engineers = session.query(cls).filter(cls.username == username).first()
            if engineers:
                return engineers.id
            else:
                return None

    @classmethod
    def get_engineers(cls):
        """Возвращает словарь c ключом - айди инженера, значение ФИО инженера"""
        with sessionfactory() as session:
            engineers = session.query(cls).all()
            if engineers:
                engineers_dict = {engineer.id: f"{engineer.last_name} {engineer.name} {engineer.patronymic}" for engineer in
                                  engineers}
                return engineers_dict
            else:
                return None

    @classmethod
    def get_fullname_by_id(cls, id: str):
        """Метод класса который добавляет инженера в базу"""
        with sessionfactory() as session:
            engineer = session.query(cls).filter_by(id=id).first()
            if engineer:
                return f'{engineer.last_name} {engineer.name} {engineer.patronymic}'
            else:
                return None

    @classmethod
    def get_engineer_data(cls, username: str):
        """Метод класса который возвращает список ФИО инженера по его username"""
        with sessionfactory() as session:
            engineer = session.query(cls).filter_by(username=username).first()
            if engineer:
                return [engineer.last_name, engineer.name, engineer.patronymic, engineer.working_position]
            else:
                return None

    @classmethod
    def get_profile_data(cls, username: str):
        """Метод класса который возвращает список ФИО и данные инженера по его username"""
        with sessionfactory() as session:
            engineer = session.query(cls).filter_by(username=username).first()
            if engineer:
                return [engineer.last_name, engineer.name, engineer.patronymic, engineer.working_position, engineer.city, engineer.phone_number, engineer.email]
            else:
                return None

    @classmethod
    def get_all_eng_data(cls):
        """Метод класса который возвращает список с данными по инженеру его направлений деятельности, количество задач,
        дату последней задачи и даты начала и конца отпуска каждого инженера"""
        data = []
        dates_of_vacations = []
        dates_of_last_tasks = []
        task_list = []
        with sessionfactory() as session:
            engineers = session.query(cls).all()
            if engineers:
                for engineer in engineers:
                    tasks_count = session.query(Task).filter(Task.engineer_id == engineer.id).count()
                    task_list.append(tasks_count)
                    last_order_date = session.query(Task.create_date).filter(Task.engineer_id == engineer.id).order_by(
                        Task.create_date.desc()).first()
                    if last_order_date is not None:
                        formatted_date = last_order_date[0].strftime('%d.%m.%Y')
                        dates_of_last_tasks.append(formatted_date)
                    else:
                        dates_of_last_tasks.append("Нет задач")
                    vacations = session.query(Vacation).filter(Vacation.engineer_id == engineer.id).first()
                    if vacations is not None:
                        vacation_dates = f'{vacations.start_date} - {vacations.end_date}'
                        dates_of_vacations.append(vacation_dates)
                    else:
                        print("Отпуск NONE")
                for i, engineer in enumerate(engineers):
                    directions = ', '.join([direction.name for direction in engineer.direction])
                    data.append([i + 1, engineer.last_name, engineer.name, engineer.patronymic, directions,
                                 engineer.working_position, engineer.city, engineer.phone_number, engineer.email, task_list[i], dates_of_last_tasks[i], dates_of_vacations[i]])
            else:
                return None
        return data

    @classmethod
    def get_username(cls, username: str):
        """Метод класса который возвращает обьект инженера по его username"""
        with sessionfactory() as session:
            engineer = session.query(cls).filter_by(username=username).first()
            if engineer:
                return engineer
            else:
                return None


class Direction(Base):
    __tablename__ = 'direction'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))
    tasks = relationship('Task', backref='direction')
    engineers = relationship("Engineer", secondary='engineer_direction', overlaps="direction")


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer(), primary_key=True)
    description = Column(String(255), nullable=False)
    direction_id = Column(Integer(), ForeignKey('direction.id'))
    status_id = Column(Integer(), ForeignKey('status.id'))
    engineer_id = Column(Integer(), ForeignKey('engineer.id'))
    create_date = Column(Date())


class Vacation(Base):
    __tablename__ = 'vacation'
    id = Column(Integer(), primary_key=True)
    engineer_id = Column(Integer(), ForeignKey('engineer.id'))
    start_date = Column(Date())
    end_date = Column(Date())


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))