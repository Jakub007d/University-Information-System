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
            conn.commit()
            return True
        else:
            cur.close()
            conn.close()
            return False



