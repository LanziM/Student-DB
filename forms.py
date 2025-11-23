from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class StudentForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    grade = StringField('Класс')
    submit = SubmitField('Сохранить')

class WorkForm(FlaskForm):
    title = StringField('Название работы', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    submit = SubmitField('Сохранить')
