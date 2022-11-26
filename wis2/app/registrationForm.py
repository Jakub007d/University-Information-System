from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    name = StringField('Meno', validators=[DataRequired()])
    address = StringField('Adresa', validators=[DataRequired()])
    s_date = StringField('Datum zaciatku studia (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Register')