from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    """Класс форма LoginForm для валидации данных для входа инженера"""
    username = StringField('Логин:', validators=[DataRequired(), Length(min=4, max=12)])
    password = PasswordField('Пароль:', validators=[DataRequired(), Length(min=5, max=16)])
    submit = SubmitField("Войти", render_kw={'class': 'btn-large'})


class AddEmployee(FlaskForm):
    """Класс форма AddEmployee для валидации и сохранения данных в бд"""
    username = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    password = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    patronymic = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    working_position = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    city = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    phone_number = StringField('phone_number', validators=[DataRequired(), Length(min=1, max=11)])
    email = StringField('email', validators=[DataRequired(), Length(min=1, max=50)])
    direction = SelectMultipleField('Направление деятельности', coerce=str)
    start_date = DateField('Начало отпуска')
    end_date = DateField('Конец отпуска')


class DeleteEmployee(FlaskForm):
    """Класс форма DeleteEmployee для валидации и удаления данных из бд"""
    employees = SelectField('Сотрудники', choices=[], coerce=str)


class EditEmployee(FlaskForm):
    """Класс форма EditEmployee для валидации и редактирования данных в бд"""
    username = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    password = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    name = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    patronymic = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    working_position = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    city = StringField('customer', validators=[DataRequired(), Length(min=1, max=50)])
    phone_number = StringField('phone_number', validators=[DataRequired(), Length(min=10, max=11)])
    email = StringField('email', validators=[DataRequired(), Length(min=1, max=50)])