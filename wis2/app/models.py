from flask_bcrypt import Bcrypt
import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-ce0ann1a6gdsa60lpc20-a.frankfurt-postgres.render.com",
        database="wis2",
        user="miguel",
        password="F8tZ8MKi3KB4gJko95puK6EB4VOPaB9s")
    return conn

def dropTableDetectionLogin(password,username):
    if "DROP TABLE" in password or "DROP TABLE" in username:
        return True
    else:
        return False

def dropTableDetection(string):
    if "DROP TABLE" in string:
        return True
    else:
        return False

class User:
    def validatePasswordAndSetUser(self,password,username):
        if dropTableDetectionLogin(password,username):
            return False
        bcript = Bcrypt()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT password FROM users WHERE login=\''+username+'\';')
        password_hash = cur.fetchone()
        if cur.rowcount != 0:
            if bcript.check_password_hash(password_hash[0],password):
                self.username = username
                return username
            else:
                return False
        else:
            return False

    def updateName(self,login,name):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET name=\''+name+'\' WHERE login=\''+login+'\';')
        conn.commit()
        cur.close()
        conn.close()

    def updateAdress(self,login,adress):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET adress=\''+adress+'\' WHERE login=\''+login+'\';')
        conn.commit()
        cur.close()
        conn.close()

    def updateEnrollment(self,login,enrollment_date):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE users SET enrollment_date=\''+enrollment_date+'\' WHERE login=\''+login+'\';')
        conn.commit()
        cur.close()
        conn.close()
    
    def fetchAllUsersLogins(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT login,login FROM users ;')
        return cur.fetchall()
    
    def updatePassword(self,name,password):
        bcript = Bcrypt()
        conn = get_db_connection()
        cur = conn.cursor()
        password_hash = bcript.generate_password_hash(password)
        if password != '':
            cur.execute('UPDATE users SET password=\''+password_hash.decode('utf8')+'\' WHERE login=\''+name+'\';')
            conn.commit()
            cur.close()
            conn.close()
        else:
            conn.commit()
            cur.close()
            conn.close()
            return False
    
    def fetchAll(self, login):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE login=\''+login+'\';')
        data = cur.fetchall()
        return data

    def registerUser(self,password,username,name,addres,s_date):
        if dropTableDetection(password) or dropTableDetection(username) or dropTableDetection(name) or dropTableDetection(addres) or dropTableDetection(s_date):
            return False
        bcript = Bcrypt()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT login FROM users WHERE login=\''+username+'\';')
        if cur.rowcount == 0:
            password = bcript.generate_password_hash(password)
            cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
                'VALUES (%s, %s, %s, %s,%s)',
                (username,
                name,
                addres,
                s_date,
                password.decode('utf8')
                )
                
            )
            conn.commit()
            cur.execute('SELECT login FROM users WHERE login=\''+username+'\';')
            if cur.rowcount != 0:
                return True
        conn.commit()
        cur.close()
        conn.close()
        return False

class Courses :
    def fetchAll(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM courses ;')
        courses = cur.fetchall()
        return courses
    
    def fetchAllGarantedCourses(self,login):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM courses WHERE login=\''+login+'\';')
        courses = cur.fetchall()
        return courses

    def fetchStudentsFromCourse(self,id_course):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_users,id_users FROM students WHERE id_course=\''+id_course+'\' and accepted=\'False\';')
        return cur.fetchall()
    
    def fetchStudentsFromTermin(self,id_termin):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_users,id_users FROM hodnotenie_studenta WHERE id_termin=\''+id_termin+'\';')
        return cur.fetchall()
    
    def fetchStudentGradesForTermin(self,id_termin):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_users,grade FROM hodnotenie_studenta WHERE id_termin=\''+id_termin+'\';')
        return cur.fetchall()

    def updateStudentStatus(self,id_student,id_course):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('UPDATE students SET accepted=TRUE WHERE id_course=\''+id_course+'\' and id_users=\''+id_student+'\';')
        conn.commit()
        cur.close()
        conn.close()

    def fetchByUsername(self,username):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM courses WHERE login=\''+username+'\';')
        courses = cur.fetchall()
        return courses

    def fetchCousesTypes(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM course_type ;')
        courses = cur.fetchall()
        return courses
    
    def fetchTerminTypes(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM termin_type ;')
        termin_type = cur.fetchall()
        return termin_type

    def fetchRooms(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM room ;')
        termin_type = cur.fetchall()
        return termin_type
    
    def addTerminToCourse(self,type,room,name,description,date,course_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO termin (type, room, name, description, date)'
                'VALUES (%s, %s, %s,%s,%s) RETURNING id',
                (type,
                room,
                name,
                description,
                date
                )
            )
        id_termin = cur.fetchall()
        id_termin = id_termin[0][0]
        print(id_termin)
        cur.execute('INSERT INTO terminy (id_course, id_termin)'
                'VALUES (%s, %s)',
                (course_id,
                id_termin
                )
            )
        conn.commit()
        cur.close()
        conn.close()

    def addStudentToCourse(self,login,course_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO students (id_course, id_users, accepted)'
                'VALUES (%s, %s,%s)',
                (course_id, login , 'FALSE')
            )
        conn.commit()
        cur.close()
        conn.close()


    def fetchCoursesNames(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name,name FROM courses ;')
        courses = cur.fetchall()
        return courses
    
    def getCourseByName(self,name):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name,login,description,accepted,price FROM courses where name=\''+name+'\';')
        courses = cur.fetchall()
        return courses

    def getCoursesByGarant(self,garant):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name,name FROM courses where login=\''+garant+'\';')
        courses = cur.fetchall()
        return courses

    def getCourseState(self,name):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT accepted FROM courses where name=\''+name+'\';')
        state = cur.fetchall()
        return state[0][0]

    def setCourseState(self,state,name):
        conn = get_db_connection()
        cur = conn.cursor()
        if state:
            cur.execute('UPDATE courses SET accepted=TRUE WHERE name=\''+name+'\';')
        else:
            cur.execute('UPDATE courses SET accepted=FALSE WHERE name=\''+name+'\';')
        conn.commit()
        cur.close()
        conn.close()
    
    def fetchCourseNews(self,id_course):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT news FROM courses where name=\''+id_course+'\';')
        state = cur.fetchall()
        return state[0][0]

    def updateTerminPoints(self,login,points,id_termin):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute('UPDATE hodnotenie_studenta SET grade=\''+points+'\' WHERE id_users=\''+login+'\' and id_termin=\''+id_termin+'\' ;')
        except:
            return False
        conn.commit()
        cur.close()
        conn.close()
        return True
    
    def isUserSignedToTermin(self,login,id_termin):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT grade FROM hodnotenie_studenta where id_termin=\''+id_termin+'\' and id_users=\''+login+'\';')
        grade = cur.fetchall()
        if cur.rowcount == 0:
            return False
        else:
            if grade[0][0] == None:
                return "-"
            return grade[0][0]
    
    def fetchTaughtCourses(self,login):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_course FROM lectors where id_users=\''+login+'\';')
        coursesIds=cur.fetchall()
        data = []
        for course in coursesIds :
            cur.execute('SELECT * FROM courses where name=\''+str(course[0])+'\';')
            if cur.rowcount == 0:
                return ""
            fetched = cur.fetchall()
            data.append(fetched)
        print(data)
        return data



    def fetchTerminById(self,id_termin):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM termin where id=\''+id_termin+'\';')
        termin = cur.fetchall()
        return termin
    
    def singStudentToTermin(self,login,id_termin):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO hodnotenie_studenta (id_termin, id_users)'
                'VALUES (%s, %s)',
                (id_termin, login)
            )
        conn.commit()
        cur.close()
        conn.close()

    
    def getTerminByCourse(self,name):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_termin FROM terminy where id_course=\''+name+'\';')
        terminCourses = cur.fetchall()
        data = []
        for termin in terminCourses :
            cur.execute('SELECT * FROM termin where id='+str(termin[0])+';')
            if cur.rowcount == 0:
                return ""
            fetched = tuple(cur.fetchall())
            data.append(fetched)
        print(data)
        return data


    def addLectorsToCourse(self,id_users,id_course):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO lectors (id_course, id_users)'
                'VALUES (%s, %s)',
                (id_course, id_users)
            )
        conn.commit()
        cur.close()
        conn.close()
    
    def fetchLectorsByCourse(self,id_course):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_users FROM lectors WHERE id_course=\''+id_course+'\';')
        return cur.fetchall()

    def fetchCoursesForStudent(self,login):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id_course FROM students WHERE id_users=\''+login+'\' and accepted=\'TRUE\';')
        courses_ids = cur.fetchall()
        courses = []
        for course in courses_ids:
           cur.execute('SELECT * FROM courses WHERE name=\''+course[0]+'\';') 
           courses.append(cur.fetchall())
        print(courses)
        return courses



    def addCourse(self,login,name,description,type):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT name FROM courses WHERE name=\''+name+'\';')
        if cur.rowcount == 0:
            cur.execute('INSERT INTO courses (name, login, type, description, accepted, price)'
                'VALUES (%s, %s, %s,%s,%s,%s)',
                (name,
                login,
                type,
                description,
                'FALSE',
                'Zadarmo'
                )
            )
            cur.execute('INSERT INTO lectors (id_course, id_users)'
                'VALUES (%s, %s)',
                (name,
                login,
                )
            )
            conn.commit()
            return True
        else:
            cur.close()
            conn.close()
            return False