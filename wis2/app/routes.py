from flask import render_template, request, redirect,url_for,flash,session
from app import app
from app.models import User ,Courses
from app.forms import LoginForm
from app.registrationForm import RegistrationForm
from flask_bcrypt import Bcrypt
import psycopg2

def getUserFromSession():
    if "user" in session:
        return session["user"]
    else:
        return ""

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
    if "user" not in session:
        if form.validate_on_submit():
            userModel = User()
            user = userModel.validatePasswordAndSetUser(form.password.data,form.username.data)
            if user == False:
                form.username.errors.append("Zle zadané dáta")
                return render_template('betterLogin.html',form=form)
            else:
                if form.remember_me.data == True:
                    session.permanent = True
                session["user"] = user
                return render_template('home.html',login = session["user"])
        else:
            return render_template('betterLogin.html',form=form)
    else:
        return redirect(url_for("homePage",login = getUserFromSession()))

@app.route('/', methods=['GET','POST'])
def mainPage():
    bcript = Bcrypt()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users;')
    users = cur.fetchall()
    conn.close()
    conn.close()
    return render_template('homePage.html',users=users , login=getUserFromSession())

@app.route('/home')
def homePage():
    if "user" in session:
        return render_template('home.html',login = getUserFromSession())
    else:
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user",None)
        return redirect(url_for("mainPage",login = getUserFromSession()))
    return redirect(url_for("mainPage",login = getUserFromSession()))

@app.route('/kurzy')
def kurzy():
    courses = Courses()
    return render_template('allCourses.html',courses = courses.fetchAll())

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        userModel = User()
        set = userModel.registerUser(form.password.data,form.username.data,form.name.data,form.address.data,form.s_date.data)
        if set == False:
            form.username.errors.append("Meno je pouzivane!")
            return render_template('registration.html',form=form)
        else:
            session["user"] = form.username.data
            return render_template('home.html',login = session["user"])
    else:
        return render_template('registration.html',form=form)
    

