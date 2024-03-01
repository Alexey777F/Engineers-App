from db import sessionfactory, engine
from flask import Flask
from datetime import timedelta
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.permanent_session_lifetime = timedelta(hours=10)
app.config['SQLALCHEMY_ENGINE'] = engine
app.config['SESSION_FACTORY'] = sessionfactory