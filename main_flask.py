import mysql.connector
from flask import Flask, redirect, render_template, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import config_data

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main_flask/home.html')


@app.route('/unfinished')
def unfinished():
    return render_template('main_flask/unfinished.html')


@app.route('/successeed')
def successeed():
    return render_template('main_flask/successeed.html')


@app.route('/registration', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        cnx = mysql.connector.connect(**config_data)
        cursor = cnx.cursor()

        user_name = request.form['name']
        phone_number = request.form['number'].translate({ord('-'): None})
        date_of_reg = datetime.now().strftime('%d-%m-%Y')
        max_id = cursor.execute("SELECT MAX(id) FROM telebot")
        id = int(cursor.fetchone()[-1]) + 1 
        new_member = (id, user_name, phone_number, None, date_of_reg)
        add_member = ("INSERT INTO telebot"
                    "(id, user_name, user_phone_number, telegram_id, date_of_reg) "
                    "VALUES (%s, %s, %s, %s, %s)")


        def check(phone_number: str):
            cursor.execute(f"SELECT user_phone_number FROM telebot WHERE user_phone_number='{phone_number}'")
            result = cursor.fetchone()
            return result
    

        try:
            if check(phone_number) is None:
                cursor.execute(add_member, new_member)
                cnx.commit()
                cursor.close()
                cnx.close()
                return redirect('/successeed')
            else: 
                return redirect('/unfinished')
        except Exception as e:
            # print(e, e.args)
            return redirect('/unfinished')            
    
    else:
        return render_template('main_flask/reg.html')


if __name__ == '__main__':
    app.run(debug=True)