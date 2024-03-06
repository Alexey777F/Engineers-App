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