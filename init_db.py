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
cur.execute('DROP TABLE IF EXISTS corses CASCADE;')
cur.execute('CREATE TABLE users (login varchar (8) NOT NULL PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'adress varchar (150) NOT NULL,'
                                 'enrollment_date date NOT NULL,'
                                 'password TEXT NOT NULL);'
                                 # TODO password budze
                                 )
cur.execute('CREATE TABLE corses (id serial PRIMARY KEY,'
                                 'login TEXT REFERENCES users (login),'
                                 'name varchar (50) NOT NULL,'
                                 'description varchar (250) NOT NULL);'
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
cur.execute('INSERT INTO corses (login, name, description)'
            'VALUES (%s, %s, %s)',
            ('xsanch00',
             'IIS', # Another great classic!
             'Tvorenie informačných systémov'
             )
            )
cur.execute('INSERT INTO corses (login, name, description)'
            'VALUES (%s, %s, %s)',
            ('admin',
             'IAS', # Another great classic!
             'Administrativa informacnych systemov'
             )
            )

conn.commit()

cur.close()
conn.close()