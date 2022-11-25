from flask import render_template, request, redirect,url_for,flash
from app import app
from app.models import User
from app.forms import LoginForm
from flask_bcrypt import Bcrypt
import psycopg2


def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-ce0ann1a6gdsa60lpc20-a.frankfurt-postgres.render.com",
        database="wis2",
        user="miguel",
        password="F8tZ8MKi3KB4gJko95puK6EB4VOPaB9s")
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        userModel = User()
        user = userModel.validatePasswordAndSetUser(form.password.data,form.username.data)
        if user == False:
            form.username.errors.append("Zle zadané dáta")
            return render_template('betterLogin.html',form=form)
        else:
            return render_template('home.html')
    else:
        return render_template('betterLogin.html',form=form)

@app.route('/', methods=['GET','POST'])
def mainPage():
    bcript = Bcrypt()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    conn.close()
    conn.close()
    print('''<h1>{{users}}</h1>''')
    return render_template('homePage.html',users=users)
