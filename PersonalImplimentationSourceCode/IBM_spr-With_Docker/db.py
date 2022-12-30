from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re

app = Flask(__name__)
app.secret_key = 'a'

conn=ibm_db.connect("DATABASE=; HOSTNAME=; PORT=; SECURITY=SSL; SSLServerCertificate=; UID=; PWD=",'','')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    global userid
    msg = ''

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = 'SELECT * FROM users WHERE username = ? AND password=?'
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin'] = True
            session['id']=account['username']
            userid = account['USERNAME']
            session['username'] = account['USERNAME']
            msg = 'Logged in Successfully!'
            return render_template('dashboard.html',msg=msg)
        else:
            msg = 'INcorrect username/password'
            return render_template('login.html',msg=msg)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['gmail']
        password = request.form['password']
        sql = "SELECT * FROM users WHERE username = ?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = "Account already exists!"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg = "Invalid email address"
        elif not re.match(r'[A-Za-z0-9]+',username):
            msg = "name must contain characters and numbers"
        else:
            insert_sql = "INSERT INTO users VALUES(?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn.insert_sql)
            ibm_db.bind_param(prep_stmt, 1, username)
            ibm_db.bind_param(prep_stmt, 2,email)
            ibm_db.bind_param(prep_stmt, 3,password)
            ibm_db.execute(prep_stmt)
            msg="You have Successfully registered"
        elif request.method == "POST":
            msg = "Please fill out the form"
            return render_template('register.html',msg = msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/apply', methods = ['GET','POST'])
def app():
    msg = ''
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        qualification = request.form['qualification']
        skills = request.form['skills']
        jobs = request.form['s']
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)

        if account():
            msg = "there is only one job position"
            return render_template('apply.html',msg = msg)
    
    insert_sql = "INSERT INTO job VALUES(?, ?, ?, ?, ?)"
    prep_stmt = ibm_db.prepare(conn, insert_sql)
    ibm_db.bind_param(prep_stmt, 1, username)
    ibm_db.bind_param(prep_stmt, 2, email)
    ibm_db.bind_param(prep_stmt, 3, qualification)
    ibm_db.bind_param(prep_stmt, 4, skills)
    ibm_db.bind_param(prep_stmt, 5, jobs)
    ibm_db.execute(prep_stmt)
    msg = "You have successfully applied for job"
    session['loggedin'] = True
    TEXT = "Hello user, a new application for job position" + jobs + isrequested

@app.route('/display')
def display():
    print session['session'],session['id']

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job WHERE userid=%s', (session['id']))
    account = cursor.fetchone()
    print('accountdisplay',account)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host = '0.0.0.0')
