from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class HomeworkAddForm(FlaskForm):
    link = StringField('Решение (Прикрепите ссылку на решение)', validators=[DataRequired()])
    number = StringField('Номер задачи', validators=[DataRequired()])
    submit = SubmitField('Отправить')
