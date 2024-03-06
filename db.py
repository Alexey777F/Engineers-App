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

    @classmethod
    def delete_engineer(cls, employee_id: str):
        """Метод класса который удаляет инженера из базы по переданному айди инженера"""
        with sessionfactory() as session:
            engineer = session.query(cls).filter_by(id=employee_id).first()
            if engineer:
                session.delete(engineer)
                vacation_records = session.query(Vacation).filter_by(engineer_id=employee_id).all()
                for record in vacation_records:
                    session.delete(record)
                try:
                    session.commit()
                    print(f"Инженер с id {employee_id} успешно удален")
                except Exception as e:
                    logger.error(f"Ошибка {e} при удалении инженера с id {employee_id}")
                    session.rollback()
            else:
                logger.error(f"Инженер с id {employee_id} не найден")

class Direction(Base):
    __tablename__ = 'direction'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))
    tasks = relationship('Task', backref='direction')
    engineers = relationship("Engineer", secondary='engineer_direction', overlaps="direction")

    @classmethod
    def add_direction(cls, name: str):
        """Метод класса который добавляет направления сотрудников в бд direction"""
        direction = cls(name=name)
        with sessionfactory() as session:
            session.add(direction)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Ошибка {e} при добавлении данных в таблицу Direction(Направления)")
                session.rollback()

    @classmethod
    def get_directions(cls):
        """Метод класса который возвращает список направлений работы сотрудников"""
        with sessionfactory() as session:
            directions = [(direction.name) for direction in session.query(cls).all()]
            if directions:
                return directions
            else:
                return None

    @classmethod
    def get_direction_id_by_name(cls, name):
        with sessionfactory() as session:
            direction_id = session.query(cls).filter(cls.name == name).first()
            if direction_id:
                return direction_id.id


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer(), primary_key=True)
    description = Column(String(255), nullable=False)
    direction_id = Column(Integer(), ForeignKey('direction.id'))
    status_id = Column(Integer(), ForeignKey('status.id'))
    engineer_id = Column(Integer(), ForeignKey('engineer.id'))
    create_date = Column(Date())

    @classmethod
    def add_task(cls, description, direction_id, status_id, engineer_id, create_date):
        """Метод класса который добавляет задачу на сотрудника"""
        task = cls(description=description, direction_id=direction_id, status_id=status_id, engineer_id=engineer_id, create_date=create_date)
        with sessionfactory() as session:
            session.add(task)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Ошибка {e} при добавлении данных в таблицу Task(Задачи)")
                session.rollback()

class Vacation(Base):
    __tablename__ = 'vacation'
    id = Column(Integer(), primary_key=True)
    engineer_id = Column(Integer(), ForeignKey('engineer.id'))
    start_date = Column(Date())
    end_date = Column(Date())

    @classmethod
    def add_vacation(cls, engineer_id, start_date, end_date):
        """Метод класса который добавляет отпуск сотруднику"""
        vacation = cls(engineer_id=engineer_id, start_date=start_date, end_date=end_date)
        with sessionfactory() as session:
            session.add(vacation)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Ошибка {e} при добавлении данных в таблицу Vacation(Отпуск)")
                session.rollback()


class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer(), primary_key=True)
    name = Column(String(50))

    @classmethod
    def add_status(cls, name):
        """Метод класса который добавляет статусы в таблицу status"""
        status = cls(name=name)
        with sessionfactory() as session:
            session.add(status)
            try:
                session.commit()
            except Exception as e:
                logger.error(f"Ошибка {e} при добавлении данных в таблицу Status(Статус)")
                session.rollback()


class EngineerCalculateMetriks:
    """Класс для фильтрации данных по разным параметрам"""
    def engineers_directions_dict(self) -> Dict:
        """Метод, который возвращает словарь {id: [список направлений}"""
        engineer_direction_dict = {}
        with sessionfactory() as session:
            engineers = session.query(Engineer).all()
            for engineer in engineers:
                engineer_direction_dict[f"{engineer.id}"] = [direction.name for direction in engineer.direction]
        return engineer_direction_dict

    def find_vacation(self, direction: str) -> List:
        """Функция в зависимости от направления и словаря с направлениями сравнивает список дат отпусков каждого инженера с сегодняшней датой"""
        date = datetime.now().strftime("%d.%m.%Y")
        potential_managers = [engineer for engineer, directions in self.engineers_directions_dict().items() if direction in directions]
        engineer_vacation_dict = {}
        for i in potential_managers:
            with sessionfactory() as session:
                vacations = session.query(Vacation).filter(Vacation.engineer_id == i).first()
                vacation_dates = [vacations.start_date + timedelta(days=x) for x in
                                  range((vacations.end_date - vacations.start_date).days + 1)]
                engineer_vacation_dict[vacations.engineer_id] = vacation_dates
        for engineer_id, dates in engineer_vacation_dict.items():
            if date in [d.strftime("%d.%m.%Y") for d in dates]:
                potential_managers.remove(str(engineer_id))
        return potential_managers

    def count_tasks(self, find_vacation: List) -> List:
        """Функция которая в зависимости от списка поданных сотрудников находит количество задач каждого сотрудника и сравнивает результат"""
        with sessionfactory() as session:
            engineer_tasks = {}
            for engineer_id in find_vacation:
                tasks_count = session.query(Task).filter(Task.engineer_id == engineer_id).count()
                engineer_tasks[engineer_id] = tasks_count if tasks_count else 0
            # Сравниваем количество задач между инженерами
            if engineer_tasks[find_vacation[0]] == engineer_tasks[find_vacation[1]]:
                return find_vacation
            else:
                # Должна вернуть список из 1-го значения - айди инженера у кого меньше заявок
                return [min(find_vacation, key=lambda x: engineer_tasks[x])]

