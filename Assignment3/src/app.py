from flask import Flask, session, redirect, url_for, escape, request, Markup, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key=b'adham'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logindatabase.db'
db = SQLAlchemy(app)



@app.route('/')
def index():
	if 'username' in session:
		return render_template('index.html')
	else:
		return 'You are not logged in'


@app.route('/lectures.html')
def lectures():
	return render_template('lectures.html')
@app.route('/index.html')
def index1():
	return render_template('index.html')

@app.route('/calender.html')
def calender():
	return render_template('calender.html')
@app.route('/Assignments.html')
def Assignments():
	return render_template('Assignments.html')
@app.route('/Feedback.html')
def Feedback():
	return render_template('Feedback.html')
@app.route('/labs.html')
def Labs():
	return render_template('Labs.html')
@app.route('/test.html')
def test():
	return render_template('test.html')
@app.route('/Resources.html')
def Resources():
	return render_template('Resources.html')



@app.route('/marks.html')
def marks():
	if 'username' in session:
			sql1 = """
						SELECT *
						FROM users
						where username='{}'""".format(session['username'])
			results = db.engine.execute(text(sql1))
			for result in results:
				if result['type'] == 'I':
					sql1 = """
						SELECT *
						FROM marks"""
				else:	
					sql1 = """
							SELECT *
							FROM marks
							where studentname='{}'""".format(session['username'])
				results = db.engine.execute(text(sql1))
			return render_template('marks.html',data=results)




@app.route('/signup',methods=['GET', 'POST'])
def signup():
	if 'username' not in session:
		if request.method=='POST':
			username=   request.form['username']
			password = request.form['password']
			updateSQL="""INSERT into users (username,password)
				   		values ('{}','{}', 'S')""".format(username,password);
			db.engine.execute(text(updateSQL))
			return render_template('index.html')






@app.route('/login',methods=['GET','POST'])
def login():
	print (request.headers.get('User-Agent')) 
	if request.method=='POST':
		sql = """
			SELECT *
			FROM users
			"""
		results = db.engine.execute(text(sql))
		for result in results:
			if result['username']==request.form['username']:
				if result['password']==request.form['password']:
					session['username']=request.form['username']
					sql1 = """
						SELECT *
						FROM marks
						where studentname='{}'""".format(request.form['username'])
					results = db.engine.execute(text(sql1))
					return render_template('index.html')
		return "Incorrect UserName/Password"
	elif 'username' in session:
			return render_template('index.html')

	else:
		return render_template('Login.html')
@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

if __name__=="__main__":
	app.run(debug=True,host='0.0.0.0')