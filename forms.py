from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Класс форма LoginForm для валидации данных для входа инженера"""
    username = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=12)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=5, max=16)])
    submit = SubmitField("Войти", render_kw={'class': 'btn-large'})