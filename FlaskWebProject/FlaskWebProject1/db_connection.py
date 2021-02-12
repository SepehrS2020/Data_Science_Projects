from datetime import datetime
from dateutil.parser import parse
import sqlite3
import time
import pyodbc


##### Connect to MS SQL Server #####


class sql_db:
    def __init__(self,form_text):
        self.form_text=form_text.strip()
        print('class initialized')

    #Connection string information
    

    def import_into_db(self):
        server='DESKTOP-SEPEHR\SQLEXPRESS'
        database='FlaskProject'
        username='sepehr'
        password='10345'
        reg_date=datetime.now().date()
        print('Establishing connection...')
        cnxn=pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + '; Trusted_Connection=yes')
        print('Connection Establishied')
        cursor=cnxn.cursor()

        print('Checking for exsiting records in database...')
        existed_records=cursor.execute(
        '''
        SELECT comment from Comments WHERE comment = ?;

        ''',(self.form_text,)
        )
        number_of_records=len(existed_records.fetchall())
        print("the number of similar existing records: ",number_of_records)

        if number_of_records>0:
            print('the comment is already existed in the database')
            print('Updating database....')
            reg_date=datetime.now().date()
            cursor.execute(
                '''
                UPDATE Comments
                SET reg_date = ?
                WHERE comment=?
                ''',
                (reg_date,self.form_text)
                )
            cnxn.commit()
            print('the time of the comment updated to {}' .format(reg_date))
            print('Data commited into database...')


        elif number_of_records==0:
            print('Importing data into database ...')
            cursor.execute(
                ''' INSERT INTO Comments (comment, reg_date) VALUES (?,?) ''',
                (self.form_text, reg_date)
                )
            cnxn.commit()
            print('Data commited into database...')
        else:
            print("do nothing")
            pass
        cnxn.close()


    # Connect to SQLite #
class sqlite_db:
    def __init__(self,form_text):
        self.form_text=form_text
    def create_database(self):
        print('Establishing connection ...')
        conn=sqlite3.connect('Flask_db.sqlite')
        cur=conn.cursor()
        print('Creating database ...')
        cur.executescript(
        '''
        CREATE TABLE IF NOT EXISTS Comments (ID INTEGER PRIMARY KEY NOT NULL UNIQUE, comment TEXT, registered_date DATETIME)
        '''
        )
        conn.close()

    def import_to_database_SQLite(self):
        #text=text.strip()
        reg_date=datetime.now().date()
        print('Establishing connection ...')
        conn=sqlite3.connect('Flask_db.sqlite')
        cur=conn.cursor()

        print('Checking for exsiting records in database...')
        existed_recors=cur.execute(
        '''
        SELECT comment from Comments WHERE comment == ?

        ''',(self.form_text,)
        )
        number_of_records=len(existed_recors.fetchall())
        print("the number of similar existing records: ",number_of_records)

        if number_of_records>0:
            print('the comment is already existed in the database')
            print('Updating database....')
            reg_date=datetime.now().date()
            cur.execute(
                '''
                UPDATE Comments
                SET registered_date = ?
                WHERE comment=?
                ''',
                (reg_date,self.form_text)
                )
            conn.commit()
            print('the time of the comment updated to {}' .format(reg_date))
            print('Commiting data into database...')


        elif number_of_records==0:
            print('Importing data into database ...')
            cur.execute(
                ''' INSERT INTO Comments (comment, registered_date) VALUES (?,?) ''',
                (self.form_text, reg_date)
                )
            conn.commit()
            print('Commiting data into database...')
        else:
            print("do nothing")
            pass
        conn.close()