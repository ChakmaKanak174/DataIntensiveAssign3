from flask import Flask, render_template, request 
import psycopg2

app = Flask(__name__)

def get_DB_connection ():
    conn1 = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="13579",
        host="localhost",
        port="5432"
    )
    return conn1

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-location', methods=['POST'])
def submit_location():
    loc = request.form['location']
    conn = get_DB_connection()
    curr = conn.cursor()

    try:
        curr.execute("SELECT * from student;",(loc,))
        St_data = curr.fetchall()

    except Exception as e:
        print("error =", e)
        St_data = []
    
    finally:
        curr.close()
        conn.close()
    
    return render_template('result.html', loc = 'location', data = St_data)

if __name__== '__main__':
    app.run(debug=True)

