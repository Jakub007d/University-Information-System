from flask_wtf import FlaskForm
from app.models import Courses
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Prihlásiť')

class UserEditForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    name = StringField('Meno', validators=[DataRequired()])
    address = StringField('Adresa', validators=[DataRequired()])
    s_date = StringField('Datum zaciatku studia (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Uložiť')

class addCourseForm(FlaskForm):
    course = Courses()
    types = course.fetchCousesTypes()
    name = StringField('Nazov kurzu', validators=[DataRequired()])
    description = StringField('Popis', validators=[DataRequired()])
    type = SelectField('Typ',choices=types)
    submit = SubmitField('Add')

class manageCourse(FlaskForm):
    course = Courses()
    names = course.fetchCoursesNames()
    courses = SelectField('Kurzy',choices=names)
    submit = SubmitField('Ukáž')

class setAcceptedCourse(FlaskForm):
    course = ''
    accepted = BooleanField('Schválené')
    update = SubmitField('Uložiť')
