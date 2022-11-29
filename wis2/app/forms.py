from flask_wtf import FlaskForm
from app.models import Courses, User
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

class garantedCoursesForm(FlaskForm):
    courses = SelectField('Garantované Kurzy')
    submit = SubmitField('Vyber')

class setAcceptedCourse(FlaskForm):
    course = ''
    accepted = BooleanField('Schválené')
    update = SubmitField('Uložiť')

class myProfile(FlaskForm):
    name = StringField('Meno')
    adress = StringField('Adresa')
    password = PasswordField('Heslo')
    enrollment_date = StringField('Dátum')
    submit = SubmitField('Ulož')

class userSelecter(FlaskForm):
    users = User()
    names = users.fetchAllUsersLogins()
    userSelector = SelectField('Uživatelia',choices=names)
    submit = SubmitField('Ukáž')

class newTermin(FlaskForm):
    type = SelectField('Typ terminu')
    room = SelectField('Miesnosť')
    name = StringField('Meno termínu')
    description = StringField('Popis')
    date = StringField('Dátum')
    submit = SubmitField('Pridať')

class submit(FlaskForm):
    submit= SubmitField("Zapísať Termin")

class students(FlaskForm):
    students = SelectField('Neschválený študenti')
    submit = SubmitField('Schváliť registráciu')

class terminEvaluationForm(FlaskForm):
    students = SelectField('Študenti zapísaný na termín')
    grade = StringField('Hodnotenie Termínu')
    submit = SubmitField('Pridat hodnotenie')

class addLectors(FlaskForm):
    userSelector = SelectField('Uživatelia')
    submit = SubmitField('Pridať lektora')