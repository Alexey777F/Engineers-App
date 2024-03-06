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

