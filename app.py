from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = "12345"

def db():
    return psycopg2.connect(
        database="student_attendance",
        user="postgres",
        password="root",
        host="localhost",
        port="5432"
    )

@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM attendance")
    records = cur.fetchall()
    con.close()

    return render_template('index.html', records=records)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        con = db()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users(name,email,password) VALUES(%s,%s,%s)",
            (request.form['name'], request.form['email'],
             request.form['password'])
        )
        con.commit()
        con.close()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        con = db()
        cur = con.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (request.form['email'], request.form['password'])
        )
        user = cur.fetchone()
        con.close()

        if user:
            session['user'] = user[0]
            return redirect('/')

    return render_template('login.html')

@app.route('/add', methods=['POST'])
def add():
    con = db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO attendance(student_name,roll_number,status) VALUES(%s,%s,%s)",
        (request.form['student_name'],
         request.form['roll_number'],
         request.form['status'])
    )
    con.commit()
    con.close()
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

app.run(debug=True)