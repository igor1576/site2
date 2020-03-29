from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class FaqAnswerForm(FlaskForm):
    answer = StringField('Напишите свой ответ', validators=[DataRequired()])
    submit = SubmitField('Отправить')
