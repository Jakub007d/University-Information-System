import os
import psycopg2
from flask_bcrypt import Bcrypt

bcript = Bcrypt()
conn = psycopg2.connect(
        host="dpg-ce0ann1a6gdsa60lpc20-a.frankfurt-postgres.render.com",
        database="wis2",
        user="miguel",
        password="F8tZ8MKi3KB4gJko95puK6EB4VOPaB9s")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users CASCADE;')
cur.execute('DROP TABLE IF EXISTS courses CASCADE;')
cur.execute('DROP TABLE IF EXISTS termin CASCADE;')
cur.execute('DROP TABLE IF EXISTS terminy CASCADE;')
cur.execute('DROP TABLE IF EXISTS course_type CASCADE;')
cur.execute('DROP TABLE IF EXISTS room CASCADE;')
cur.execute('DROP TABLE IF EXISTS lectors CASCADE;')
cur.execute('DROP TABLE IF EXISTS students CASCADE;')
cur.execute('DROP TABLE IF EXISTS termin_type CASCADE;')
cur.execute('DROP TABLE IF EXISTS hodnotenie_studenta CASCADE;')


cur.execute('CREATE TABLE users (login varchar (8) NOT NULL PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'adress varchar (150) NOT NULL,'
                                 'enrollment_date date NOT NULL,'
                                 'password TEXT NOT NULL);'
                                 # TODO password budze
                                 )

cur.execute('CREATE TABLE course_type (id serial PRIMARY KEY,'
                                 'name varchar (50) NOT NULL);'
                                 )
cur.execute('CREATE TABLE courses (name varchar (50) NOT NULL PRIMARY KEY,'
                                 'login varchar (8) REFERENCES users (login),'
                                 'type int REFERENCES course_type (id),'
                                 'description varchar (250),'
                                 'accepted BOOLEAN NOT NULL,'
                                 'price varchar (250),'
                                 'news varchar (250) );'
                                 )

cur.execute('CREATE TABLE room (id SERIAL PRIMARY KEY,'
                                 'name varchar (50) NOT NULL);'
                                 )
cur.execute('CREATE TABLE termin_type (id SERIAL PRIMARY KEY,'
                                 'name varchar (50) NOT NULL);'
                                 )
cur.execute('CREATE TABLE termin (id SERIAL PRIMARY KEY,'
                                 'type int REFERENCES termin_type (id),'
                                 'room int REFERENCES room (id),'
                                 'name varchar (50) NOT NULL,'
                                 'description varchar (250),'
                                 'date date NOT NULL);'
                                 )

cur.execute('CREATE TABLE lectors (id_course varchar (50) REFERENCES courses (name),'
                                 'id_users varchar (8) REFERENCES users (login),'
                                 'PRIMARY KEY(id_course, id_users));'
                                 )
cur.execute('CREATE TABLE terminy (id_course varchar (50) REFERENCES courses (name),'
                                 'id_termin int REFERENCES termin (id),'
                                 'PRIMARY KEY(id_course, id_termin));'
                                 )
cur.execute('CREATE TABLE students (id_course varchar (50) REFERENCES courses (name),'
                                 'id_users varchar (8) REFERENCES users (login),'
                                 'PRIMARY KEY(id_course, id_users));'
                                 )
cur.execute('CREATE TABLE hodnotenie_studenta (id_termin int REFERENCES termin (id),'
                                 'id_users varchar (8) REFERENCES users (login),'
                                 'grade int,'
                                 'PRIMARY KEY(id_termin, id_users));'
                                 )
# Insert data into the table


heslo = bcript.generate_password_hash('chorizo')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('xsanch00',
             'Miguel Sanches',
             'Ulica De la Cruise numero seis, Madrid, Espanol',
             '2019-09-14',
             heslo.decode('utf8')
             )
            )
heslo = bcript.generate_password_hash('tank')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('xszlot01',
             'Jocko Szlota', # Another great classic!
             'Ulica Andreja Hlinku 420, Zilina, 96885, Slotovisko',
             '2012-08-31',
              heslo.decode('utf8')
            )
)
heslo = bcript.generate_password_hash('ugabouga')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('xkokot00',
             'Ultra Kokot', # Another great classic!
             'Ulica Odpadlisko dejiin 12, Margecany, 98888, Slovensko',
             '2025-08-31',
             heslo.decode('utf8')
             )
            )
heslo = bcript.generate_password_hash('1111')
cur.execute('INSERT INTO users (login, name, adress, enrollment_date,password)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('admin',
             'Ignac Vsetkovie', # Another great classic!
             'Ulica Kukucinova 12, Vychodne, 98458, Slovensko',
             '1999-08-31',
             heslo.decode('utf8')
             )
            )

cur.execute('INSERT INTO course_type (name)'
            'VALUES(\'prezenčne\')'
            )
cur.execute('INSERT INTO course_type (name)'
            'VALUES(\'distančne\')'
            )
cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Polsemestrálny Test\')'
            )
cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Zaverečná skúška\')'
            )
cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Projekt\')'
            )
cur.execute('INSERT INTO courses (name, login, type, description, accepted, price)'
            'VALUES (%s, %s, %s, %s,%s,%s)',
            ('IAS',
             'admin', # Another great classic!
             '1',
             'Správa informačného systému',
             'TRUE',
             'Zadarmo'
             )
            )
cur.execute('INSERT INTO courses (name, login, type, description, accepted, price)'
            'VALUES (%s, %s, %s, %s,%s,%s)',
            ('IIS',
             'xsanch00', # Another great classic!
             '1',
             'Tvorenie informacného systému',
             'TRUE',
             'Zadarmo'
             )
            )
cur.execute('INSERT INTO room (name)'
            'VALUES(\'D105\')'
            )

cur.execute('INSERT INTO room (name)'
            'VALUES(\'D215\')'
            )
cur.execute('INSERT INTO room (name)'
            'VALUES(\'L101\')'
            )

cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Domáca uloha\')'
            )
cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Projekt\')'
            )
cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Polsemestrálny test\')'
            )
cur.execute('INSERT INTO termin_type (name)'
            'VALUES(\'Záverečná skúška\')'
            )
cur.execute('INSERT INTO termin (type, room, name, description, date)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('3',
             '1', # Another great classic!
             'Polsemestrálny test',
             'Test z prvých 3 látok predmetu',
             '2022-12-12'
             )
            )
cur.execute('INSERT INTO termin (type, room, name, description, date)'
            'VALUES (%s, %s, %s, %s,%s)',
            ('3',
             '1', # Another great classic!
             'Polsemestrálny test 2. skupina',
             'Test z prvých 3 látok predmetu',
             '2022-12-12'
             )
            )
cur.execute('INSERT INTO lectors (id_course, id_users)'
            'VALUES (%s, %s)',
            ('IAS',
             'xsanch00' # Another great classic!
             )
            )
cur.execute('INSERT INTO terminy (id_course, id_termin)'
            'VALUES (%s, %s)',
            ('IAS',
             '1' # Another great classic!
             )
            )
cur.execute('INSERT INTO terminy (id_course, id_termin)'
            'VALUES (%s, %s)',
            ('IAS',
             '2' # Another great classic!
             )
            )              
conn.commit()

cur.close()
conn.close()