from flask import render_template, request, redirect,url_for,flash,session
from app import app
from app.models import User ,Courses
from app.forms import LoginForm,addCourseForm,manageCourse,setAcceptedCourse,UserEditForm,myProfile
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
    coursesModel = Courses()
    courses = coursesModel.fetchAll()
    return render_template('homePage.html',courses=courses , login=getUserFromSession())

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



@app.route("/správa_serveru", methods=['GET', 'POST'])
def spravaServeru():
    form = manageCourse()
    form2 = setAcceptedCourse()
    courseModel = Courses()
    form.courses.choices = courseModel.fetchCoursesNames()
    if form.validate_on_submit():
        courses = courseModel.getCourseByName(form.courses.data)
        form2.accepted.data=courseModel.getCourseState(form.courses.data)
        session["course"] = form.courses.data
        return render_template('sprava_serveru.html',form=form,course=courses,form2=form2)
    if form2.validate_on_submit():
        courseModel.setCourseState(form2.accepted.data,session["course"])
        return render_template('sprava_serveru.html',form=form,course='',form2=form2)
    return render_template('sprava_serveru.html',form=form,course='',form2=form2)

@app.route("/my_profile", methods=['GET', 'POST'])
def mojProfil():
    form = myProfile()
    userModel = User()
    data = userModel.fetchAll(getUserFromSession())
    if form.validate_on_submit():
        name = form.name.data
        adress = form.adress.data
        password = form.password.data
        enrollment_date = form.enrollment_date.data
        if name != "":
            userModel.updateName(getUserFromSession(),name)
        if name != "":
            userModel.updateAdress(getUserFromSession(),adress)
        if password != "":
            userModel.updatePassword(getUserFromSession(),password)
        if name != "":
            userModel.updateEnrollment(getUserFromSession(),enrollment_date)
        return redirect(url_for("mainPage",login = getUserFromSession()))
    form.name.data = data[0][1]
    form.adress.data = data[0][2]
    form.enrollment_date.data = data[0][3]
    return render_template('myProfile.html',form=form, login = getUserFromSession())


@app.route("/add_course", methods=['GET', 'POST'])
def addCourse():
    form = addCourseForm()
    if form.validate_on_submit():
        courseModel = Courses()
        set = courseModel.addCourse(getUserFromSession(),form.name.data,form.description.data,form.type.data)
        if set == False:
            form.name.errors.append("Meno je pouzivane!")
            return render_template('add_course.html',form=form)
        else:
            return render_template('home.html',login = session["user"])
    else:
        return render_template('add_course.html',form=form)