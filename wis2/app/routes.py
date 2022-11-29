from flask import render_template, request, redirect,url_for,flash,session
from app import app
from app.models import User ,Courses
from app.forms import LoginForm,addCourseForm,manageCourse,setAcceptedCourse,UserEditForm,myProfile,userSelecter,garantedCoursesForm,newTermin, submit , students, addLectors, terminEvaluationForm, addRoomForm , newNews
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
@app.route('/garanted_courses',methods=['GET', 'POST'])
def garantedCourses():
    courseModel = Courses()
    courses = courseModel.fetchAllGarantedCourses(getUserFromSession())
    return render_template('garanted_courses.html',courses=courses)

@app.route('/add_lector',methods=['GET', 'POST'])
def addLector():
    courseModel=Courses()
    usersModel = User()
    form = addLectors()
    data = request.form
    data = data.getlist('course')
    try:
        data = data[0]
        session["kurz"] = data
    except:
        data = session["kurz"]
    form.userSelector.choices = usersModel.fetchAllUsersLogins()
    if form.validate_on_submit():
        courseModel.addLectorsToCourse(form.userSelector.data,data)
        return redirect(url_for("addLector"))
    lectors = courseModel.fetchLectorsByCourse(data)
    return render_template('course_lectors.html',form=form,login=getUserFromSession(),lectors=lectors)
    


@app.route('/course_editing')
def courseEditing():
    courseModel = Courses()
    terminy = courseModel.getTerminByCourse(session["kurz"])
    if terminy != "":
        print(terminy)
        terminy.sort()
        return render_template('course_editing.html',terminy=terminy,course = session["kurz"],login = getUserFromSession())
    else:
        return render_template('course_editing.html',terminy="",course = session["kurz"],login = getUserFromSession())

@app.route('/course_detail',methods=['GET', 'POST'])
def courseDetail():
    data = request.form
    data = data.getlist('param1')
    data = data[0]
    courseModel = Courses()
    terminy = courseModel.getTerminByCourse(data)
    session["kurz"] = data
    if terminy != "":
        print(terminy)
        terminy.sort()
        return render_template('course_editing.html',terminy=terminy,course=data,login=getUserFromSession())
    else:
        return render_template('course_editing.html',terminy="",course=data,login=getUserFromSession())

@app.route('/add_student',methods=['GET', 'POST'])
def addStudent():
    courseModel = Courses()
    courseModel.addStudentToCourse(getUserFromSession(),session["kurz"])
    return redirect(url_for("mainPage"))


@app.route('/', methods=['GET','POST'])
def mainPage():
    coursesModel = Courses()
    courses = coursesModel.fetchAll()
    coursesModel.fetchCoursesForStudent(getUserFromSession())
    return render_template('homePage.html',courses=courses , login=getUserFromSession())
@app.route('/my_courses',methods=['GET','POST'])
def myCourses():
    courseModel = Courses()
    courses = courseModel.fetchCoursesForStudent(getUserFromSession())
    return render_template('my_courses.html',courses=courses)

@app.route('/add_termin', methods=['GET','POST'])
def addTermin():
    form = newTermin()
    form1 = newNews()
    coursesModel = Courses()
    course_id = request.form
    course_id = course_id.getlist('course')
    try:
        course_id = course_id[0]
        session["kurz"] = course_id
    except:
        if "kurz" in session:
            course_id = session["kurz"]
        else:
            course_id=""
    form.type.choices = coursesModel.fetchTerminTypes()
    form.room.choices = coursesModel.fetchRooms()
    if form.validate_on_submit and form.name.data != None:
        coursesModel.addTerminToCourse(form.type.data,form.room.data,form.name.data,form.description.data,form.date.data,course_id)
        return redirect(url_for("homePage"))
    
    if form1.validate_on_submit():
        coursesModel.addNewsToCourse(form1.news.data,course_id)
    return render_template("termin_add.html",form=form,course=course_id,form1=form1)


@app.route('/accept_student',methods=['GET','POST'])
def acceptStudent():
    data = request.form
    data = data.getlist('course')
    try:
        data = data[0]
        session["kurz"] = data
    except:
        data = session["kurz"]
    form = students()
    courseModel = Courses()
    form.students.choices = courseModel.fetchStudentsFromCourse(data)
    if form.validate_on_submit():
        courseModel.updateStudentStatus(form.students.data,data)
        return redirect(url_for("acceptStudent"))
    return render_template('accept_students.html',form=form,login=getUserFromSession())

    


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


@app.route("/add_room",methods=['GET','POST'])
def addRoom():
    form = addRoomForm()
    courseModel = Courses()
    if form.validate_on_submit():
        courseModel.addRoomModel(form.room.data)
        return redirect(url_for("addRoom"))
    return render_template("add_room.html",form=form)
    


@app.route('/kurzy')
def kurzy():
    courses = Courses()
    return render_template('allCourses.html',courses = courses.fetchAll())

@app.route('/manage_users', methods=['GET', 'POST'])
def manageUsers():
    form = userSelecter()
    usersModel = User()
    form.userSelector.choices = usersModel.fetchAllUsersLogins()
    if form.validate_on_submit():
        pass
        data = usersModel.fetchAll(form.userSelector.data)
    if form.validate_on_submit():
        session["updated_user"] =form.userSelector.data
        return redirect(url_for('manageUser'))
    return render_template('manage_users.html',form=form)

@app.route('/manage_user', methods=['GET', 'POST'])
def manageUser():
    form1 = myProfile()
    userModel = User()
    updated_user = " "
    if "updated_user" in session:
        updated_user = session["updated_user"]
    data = userModel.fetchAll(updated_user)
    if form1.validate_on_submit and form1.name.data != None:
        name = form1.name.data
        print(name)
        adress = form1.adress.data
        password = form1.password.data
        enrollment_date = form1.enrollment_date.data
        if name != "":
            userModel.updateName(updated_user,name)
        if name != "":
            userModel.updateAdress(updated_user,adress)
        if password != "":
            userModel.updatePassword(updated_user,password)
        if name != "":
            userModel.updateEnrollment(updated_user,enrollment_date)
        return redirect(url_for("mainPage",login = getUserFromSession()))
    form1.name.data = data[0][1]
    form1.adress.data = data[0][2]
    form1.enrollment_date.data = data[0][3]
    return render_template('myProfile.html',form=form1, login = updated_user)
    


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

@app.route("/atended_course",methods=['GET', 'POST'])
def atendedCourse():
    courseModel=Courses()
    data = request.form
    data = data.getlist('course')
    try:
        data = data[0]
        session["kurz"] = data
    except:
        data = session["kurz"]
    terminy = courseModel.getTerminByCourse(data)
    news = courseModel.fetchCourseNews(data)
    if news is None:
        news = "Žiadne novinky"
    return render_template('atended_course.html',terminy=terminy,news=news,course=data)

@app.route("/taught_courses",methods=['GET', 'POST'])
def taughtCourses():
    courseModel=Courses()
    myCourses=courseModel.fetchTaughtCourses(getUserFromSession())
    return render_template("taught_courses.html",courses=myCourses,login=getUserFromSession())

@app.route("/terminy_for_lector",methods=['GET', 'POST'])
def terminyForLector():
    courseModel=Courses()
    data = request.form
    data = data.getlist('course')
    try:
        data = data[0]
        session["kurz"] = data
    except:
        data = session["kurz"]
    terminy = courseModel.getTerminByCourse(data)
    print (terminy)
    return render_template("terminy_for_lector.html",terminy=terminy,course=data)

@app.route("/termin_evaluation",methods=['GET', 'POST'])
def terminEvaluation():
    form = terminEvaluationForm()
    courseModel = Courses()
    data = request.form
    data = data.getlist('termin')
    try:
        data = data[0]
        session["termin"] = data
    except:
        data = session["termin"]
    form.students.choices = courseModel.fetchStudentsFromTermin(data)
    grades = courseModel.fetchStudentGradesForTermin(data)
    if form.validate_on_submit():
        fail = courseModel.updateTerminPoints(form.students.data,form.grade.data,data)
        if fail == False:
            form.grade.errors.append("Zlý formát hodnotenia")
        return redirect(url_for("terminEvaluation"))
    return render_template("grade_termin.html",grades=grades,form=form)
    


@app.route("/termin_detail",methods=['GET', 'POST'])
def terminDetail():
    courseModel=Courses()
    form=submit()
    data = request.form
    data = data.getlist('termin')
    try:
        data = data[0]
        session["termin"] = data
    except:
        data = session["termin"]
    grade = courseModel.isUserSignedToTermin(getUserFromSession(),data)
    if grade == False:
        grade="None"
    termin = courseModel.fetchTerminById(data)
    if form.validate_on_submit():
        courseModel.singStudentToTermin(getUserFromSession(),data)
        return redirect(url_for("terminDetail"))
    return render_template("termin_student_detail.html",form=form,grade=grade,termin=termin)
    
    
    

    



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