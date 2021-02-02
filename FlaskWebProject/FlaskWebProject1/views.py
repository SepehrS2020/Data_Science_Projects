"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, jsonify, url_for, request
from FlaskWebProject1 import app
import requests
import pandas as pd
from dateutil.parser import parse
import sqlite3
import time



@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    print("Contact calling....")
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )


@app.route('/text', methods = ['GET', 'POST'])
def text():
    """Renders the text page."""

    def create_database():
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



    def import_to_database(form_text):
        #text=text.strip()
        reg_date=datetime.now().date()
        print('Establishing connection ...')
        conn=sqlite3.connect('Flask_db.sqlite')
        cur=conn.cursor()

        print('Checking for exsiting records in database...')
        existed_recors=cur.execute(
        '''
        SELECT comment from Comments WHERE comment == ?

        ''',(form_text,)
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
                (reg_date,form_text)
                )
            conn.commit()
            print('the time of the comment updated to {}' .format(reg_date))
            print('Commiting data into database...')


        elif number_of_records==0:
            print('Importing data into database ...')
            cur.execute(
                ''' INSERT INTO Comments (comment, registered_date) VALUES (?,?) ''',
                (form_text, reg_date)
                )
            conn.commit()
            print('Commiting data into database...')
        else:
            print("do nothing")
            pass
        conn.close()

    if request.method == "POST":
        form_comment=request.form.get("comments")
        form_comment=str(form_comment)
        #form_comment='this1'
        print(type(form_comment))
        print("the {} has been entered into the comment area" .format(form_comment))
        create_database()
        import_to_database(form_comment)
    else:
        pass



    #forms=request.post('https://solutions')
    return render_template(
        'text.html',
        title='Text',

        year=datetime.now().year,
        message='Your text description page.'
    )








@app.route('/solutions', methods = ['GET', 'POST'])
def solutions():
    """Renders the solutions page."""
    url='https://hooks.bluebrain.xyz/api/v1/za/sales?start=2020-1-27&end=2020-11-28'
    r = requests.get(url, headers={'Authorization': '6SIFsKEjeHe214NDy2lNeDP39BRzHUpzZI6t5R214NDy26TkrwuErQ8mbw2yVzMMatJbZe51VCzYCSyM1kvoe1qWhbE7xPSwdDeA'})
    incomming_data=r.json()
    columnNames=['vendor_name', 'model_name', 'object_pur_articlePrice', 'object_sale_datePurchase',
     'object_sale_articlePriceTotal', 'caseMaterial', 'cycleTime']
    form_start_date='2020-01-01'
    form_end_date='2020-01-29'



    def create_database():
        print('Establishing connection ...')
        conn=sqlite3.connect('Flask_db.sqlite')
        cur=conn.cursor()
        print('Creating database ...')
        cur.executescript(
        '''
        CREATE TABLE IF NOT EXISTS Sales (vendor_name TEXT, model_name TEXT,
        object_pur_articlePrice FLOAT, object_sale_datePurchase DATETIME,
        object_sale_articlePriceTotal FLOAT, caseMaterial TEXT, cycleTime DATETIME)
        '''
        )
        conn.close()



    def import_to_database(data):
        print('Establishing connection ...')
        conn=sqlite3.connect('Flask_db.sqlite')
        cur=conn.cursor()
        print('Importing data into database ...')
        count=0
        for item in data:
            cur.execute(
            '''
            INSERT INTO Sales (vendor_name, model_name, object_pur_articlePrice,
            object_sale_datePurchase, object_sale_articlePriceTotal, caseMaterial, cycleTime)
            VALUES (?, ?, ?, ?, ?, ?, ?) ''',
            (
            item['vendor_name'], item['model_name'],item['object_pur_articlePrice'],
            item['object_sale_datePurchase'], item['object_sale_articlePriceTotal'],
            item['caseMaterial'], item['cycleTime']   )
            )
            conn.commit()
            count+=1
            if count % 10 == 0 :
                print('Commiting data into database...')
                time.sleep(5)
        conn.close()

    # DataFrame
    #data= pd.DataFrame(r.json())
    #export_table=data.to_html(classes='data')

    #data=data[data['object_pur_datePayment']<'2019']

    #data=incomming_data
    if request.method == "POST":
        form_name = request.form.get('form_name')
        if form_name == 'sales_table':
            form_start_date=request.form.get('start_date')
            form_end_date=request.form.get('end_date')
            print("the range of the data was set {} and {}" .format(form_start_date,form_end_date))
            data = [d for d in incomming_data if parse(d.get("object_sale_datePurchase"))<=parse(form_end_date) and parse(d.get("object_sale_datePurchase"))>=parse(form_start_date) ]
        if form_name == 'save_data':
            data = [d for d in incomming_data if parse(d.get("object_sale_datePurchase"))<=parse(form_end_date) and parse(d.get("object_sale_datePurchase"))>=parse(form_start_date) ]
            create_database()
            import_to_database(data)
        else:
            pass



    #forms=request.post('https://solutions')
    return render_template(
        'solutions.html',
        title='Solutions',
        form_start_date=form_start_date,
        form_end_date=form_end_date,
        records=data,
        colnames=columnNames,

        #export_table=export_table,
        #titles=data.columns.values,

        year=datetime.now().year,
        message='Your solutions description page.'
    )

@app.route('/api/message')
def message():
    """Renders the about page."""
    return jsonify({
        "username":"sepehr",
        "email":"sepehr@gmail.com",
        "id":"id"}
    )

#https://hooks.bluebrain.xyz/api/v1/za/sales?start=2020-1-27&end=2020-11-28
#header: authorization:
