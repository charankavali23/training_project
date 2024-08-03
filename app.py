from flask import Flask, render_template, request, redirect, url_for, session
from psycopg2 import connect
import re
import yaml

app = Flask(__name__)

# Load configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

app.secret_key = config['app']['secret_key']

def db_connection():
    conn = connect(
        dbname=config['database']['dbname'],
        user=config['database']['user'],
        password=config['database']['password'],
        host=config['database']['host'],
        port=config['database']['port']
    )
    cur = conn.cursor()
    return conn, cur

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conn, cur = db_connection()
        cur.execute(f"SELECT * FROM public.authentication_details WHERE email='{email}' AND password=crypt('{password}', password);")
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = int(user[0])
            session['name'] = user[1]
            session['email'] = user[3]
            message = 'Logged in successfully!'
            cur.close()
            conn.close()
            return render_template('user.html', message=message)
        else:
            cur.close()
            conn.close()
            message = 'Please enter correct email / password!'
    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        conn, cur = db_connection()
        cur.execute(f"SELECT * FROM public.authentication_details WHERE email='{email}';")
        account = cur.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            cur.execute(f"INSERT INTO public.authentication_details (name, password, email) VALUES ('{userName}', crypt('{password}', gen_salt('bf')), '{email}');")
            conn.commit()
            message = 'You have successfully registered!'
        cur.close()
        conn.close()
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('register.html', message=message)

if __name__ == "__main__":
    app.run(host="0.0.0.0")