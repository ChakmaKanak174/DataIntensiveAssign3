from flask import Flask, render_template, request 
import psycopg2
import mysql.connector 
from flask_mysqldb import MySQL


app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12321'
app.config['MYSQL_DB'] = 'lahtidb'            

mysql1 = MySQL(app)

def get_kouvola_connection():
    conn = MySQL()
    conn.init_app(app)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '12321'
    app.config['MYSQL_DB'] = 'kouvoladb'
    return conn

def get_pg_connection ():
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="13579",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-location', methods=['POST'])
def submit_location():
    loc = request.form['location']

    if loc == 'Lahti':
        curr = mysql1.connection.cursor()

    elif loc == 'Lappenranta':
        conn = get_pg_connection()
        curr = conn.cursor()

    elif loc == 'Kouvola':
        mysql2 = get_kouvola_connection()
        curr = mysql2.connection.cursor()

    try:
        curr.execute("SELECT * from student;")
        St_data = curr.fetchall()

    except Exception as e:
        print("error =", e)
        St_data = []
    
    finally:
        curr.close()
    
    return render_template('result.html', loc = loc, data = St_data)



if __name__== '__main__':
    app.run(debug=True)