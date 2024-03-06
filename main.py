from datetime import datetime
from flask import render_template, redirect, flash, url_for, session
from forms import LoginForm, AddEmployee, EditEmployee, DeleteEmployee, AddTask
from db import Direction, Engineer, Vacation, Task, EngineerCalculateMetriks
from functools import wraps
from typing import Callable
from app_config import app
from sqlalchemy.exc import OperationalError
from logger_conf import Logger