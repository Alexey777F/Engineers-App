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