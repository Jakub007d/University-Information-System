import os
import psycopg2

conn = psycopg2.connect(
        host="postgres://miguel:F8tZ8MKi3KB4gJko95puK6EB4VOPaB9s@dpg-ce0ann1a6gdsa60lpc20-a.frankfurt-postgres.render.com/wis2",
        database="wis2",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS user;')
cur.execute('CREATE TABLE user (id serial PRIMARY KEY,'
                                 'login varchar (8) NOT NULL,'
                                 'name varchar (150) NOT NULL,'
                                 'adress varchar (150) NOT NULL,'
                                 'enrollment_date date NOT NULL);'
                                 # TODO password budze
                                 )

# Insert data into the table

cur.execute('INSERT INTO user (login, name, adress, enrollment_date)'
            'VALUES (%s, %s, %s, %s)',
            ('xsanch00',
             'Miguel Sanches',
             'Ulica De la Cruise numero seis, Madrid, Espanol',
             '2019-09-14')
            )

cur.execute('INSERT INTO user (login, name, adress, enrollment_date)'
            'VALUES (%s, %s, %s, %s)',
            ('xszlot01',
             'Jocko Szlota', # Another great classic!
             'Ulica Andreja Hlinku 420, Zilina, 96885, Slotovisko',
             '2012-08-31')
            )

cur.execute('INSERT INTO user (login, name, adress, enrollment_date)'
            'VALUES (%s, %s, %s, %s)',
            ('xkokot00',
             'Ultra Kokot', # Another great classic!
             'Ulica Odpadlisko dejiin 12, Margecany, 98888, Slovensko',
             '2025-08-31')
            )

conn.commit()

cur.close()
conn.close()