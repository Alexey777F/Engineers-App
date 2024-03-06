from datetime import datetime
from flask import render_template, redirect, flash, url_for, session
from forms import LoginForm, AddEmployee, EditEmployee, DeleteEmployee, AddTask
from db import Direction, Engineer, Vacation, Task, EngineerCalculateMetriks
from functools import wraps
from typing import Callable
from app_config import app
from sqlalchemy.exc import OperationalError
from logger_conf import Logger

logger = Logger()


def set_engineer_session(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if 'username' in session:
                username = session['username']
                engineer_info = Engineer.get_engineer_data(username)
                if engineer_info:
                    engineer_name = ' '.join(engineer_info[0:3])
                    working_position = engineer_info[3]
                    short_name = engineer_info[1][0] + '. ' + engineer_info[0]
                    return func(username, engineer_name, working_position, short_name, *args, **kwargs)
        except OperationalError as e:
            logger.error(f"Ошибка соединения с бд! {e}")
            return redirect(url_for('db_error'))
        return redirect(url_for('login'))
    return wrapper


@app.route('/')
def index():
    """Роутер / который редиректит на login"""
    return redirect(url_for('login'), 302)


@app.route('/db_error')
def db_error():
    return render_template('db_error.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """Роутер /login, который рендерит страницу login.html и при успешной проверке - редиректит на функцию admin_main"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        # Проверяем наличие пользователя в базе данных
        try:
            engineer = Engineer.get_username(username)
            if engineer:
                if password == engineer.password:
                    # Логин и пароль совпадают
                    session['username'] = username
                    return redirect(url_for('admin_main'))
                else:
                    # Пароль не совпадает
                    flash("Неверный пароль")
            else:
                flash("Пользователь не найден")
        except OperationalError as e:
            logger.error(f"Ошибка соединения с бд! {e}")
            return redirect(url_for('db_error'))
    return render_template("login.html", title="Вход", form=form)


@app.route('/admin/main', methods=["POST", "GET"])
@set_engineer_session
def admin_main(username, engineer_name, working_position, short_name):
    """Роутер /admin_main, который отображает главную страницу"""
    engineer_data = Engineer.get_all_eng_data()
    return render_template("admin_main.html", username=username, engineer_name=engineer_name, working_position=working_position,
                            short_name=short_name, engineer_data=engineer_data)


@app.route('/admin/employee', methods=["POST", "GET"])
@set_engineer_session
def admin_employee(username, engineer_name, working_position, short_name):
    """Роутер /admin_employee, который отображает страницу с данными сотрудников"""
    engineer_data = Engineer.get_all_eng_data()
    return render_template("admin_employee.html", username=username, engineer_name=engineer_name, working_position=working_position,
                            short_name=short_name, engineer_data=engineer_data)


@app.route('/admin/add_task', methods=["POST", "GET"])
@set_engineer_session
def add_task(username, engineer_name, working_position, short_name):
    """Роутер /add_task, который проверят ввод данных из формы и назначает соответствующего направлению, сотрудника"""
    form = AddTask()
    form.direction.choices = Direction.get_directions()
    if form.validate_on_submit():
        direction = form.direction.data
        description = form.description.data
        engineer_calculate = EngineerCalculateMetriks()
        potential_engineers = engineer_calculate.find_vacation(direction)
        direction_id = Direction.get_direction_id_by_name(direction)
        today = datetime.now()
        # 1) вычисляются потенциальные инженеры на задачу - список [3, 5] айдишники инженеров
        if len(potential_engineers) > 1:
            tasks_count_result = engineer_calculate.count_tasks(potential_engineers)
            if len(tasks_count_result) > 1:
                # compare_last_orders_result = engineer_calculate.compare_last_orders(tasks_count_result)
                id = engineer_calculate.compare_last_orders(tasks_count_result)
                Task.add_task(description, direction_id, 1, id, today)
                flash(f'Задачу направления {direction} - назначаем на инженера - ' + Engineer.get_fullname_by_id(id), 'success')
            elif len(tasks_count_result) == 1:
                id = tasks_count_result[0]
                Task.add_task(description, direction_id, 1, id, today)
                flash(f'Задачу направления {direction} - назначаем на инженера - ' + Engineer.get_fullname_by_id(id), 'success')
        elif len(potential_engineers) == 1:
            id = potential_engineers[0]
            Task.add_task(description, direction_id, 1, id, today)
            flash(f'Задачу направления {direction} - назначаем на инженера - ' + Engineer.get_fullname_by_id(id), 'success')
        else:
            flash(f'На данный момент на задачу: {direction}, нет инженеров!', 'error')
        return redirect(url_for('add_task'))
    return render_template("add_task.html", username=username,
                                            engineer_name=engineer_name,
                                            working_position=working_position,
                                            short_name=short_name, form=form)


@app.route('/admin/employee/add_employee', methods=["POST", "GET"])
@set_engineer_session
def add_employee(username, engineer_name, working_position, short_name):
    """Роутер /add_employee, который содержит форму добавления сотрудника в бд"""
    form = AddEmployee()
    form.direction.choices = Direction.get_directions()
    if form.validate_on_submit():
        username_form = form.username.data
        password = form.password.data
        last_name = form.last_name.data
        name = form.name.data
        patronymic = form.patronymic.data
        working_position = form.working_position.data
        city = form.city.data
        phone_number = form.phone_number.data
        email = form.email.data
        choice_directions = form.direction.data
        date = datetime.now()
        start_date = datetime.strptime(str(form.start_date.data), '%Y-%m-%d').date()
        end_date = datetime.strptime(str(form.end_date.data), '%Y-%m-%d').date()
        Engineer.add_engineer(username=username_form, password=password, last_name=last_name, name=name,
                              patronymic=patronymic, working_position=working_position, city=city,
                              phone_number=phone_number, email=email, created_on=date)
        Engineer.add_engineer_directions(username_form, last_name, choice_directions)
        engineer = Engineer.get_id_by_username(username_form)
        Vacation.add_vacation(engineer, start_date, end_date)
        flash(f'Данные инженера: {last_name} {name} {patronymic} успешно добавлены!', 'success')
        return redirect(url_for("add_employee"))
    return render_template("add_employee.html", username=username, engineer_name=engineer_name,
                           working_position=working_position, short_name=short_name, form=form)


@app.route('/admin/employee/edit_employee', methods=["POST", "GET"])
@set_engineer_session
def edit_employee(username, engineer_name, working_position, short_name):
    """Роутер /edit_employee, который форму редактирования для сотрудника"""
    form = EditEmployee()
    if form.validate_on_submit():
        username_form = form.username.data
        password = form.password.data
        last_name = form.last_name.data
        name = form.name.data
        patronymic = form.patronymic.data
        working_position = form.working_position.data
        city = form.city.data
        phone_number = form.phone_number.data
        email = form.email.data
        # запись в бд
        return redirect(url_for("admin_employee"))
    return render_template("edit_employee.html", username=username, engineer_name=engineer_name,
                           working_position=working_position, short_name=short_name, form=form)
