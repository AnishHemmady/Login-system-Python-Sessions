'''
Login system using python and mongodb
'''
from flask import Flask, render_template, url_for, request, session, redirect
from flask.ext.pymongo import PyMongo
import bcrypt

app = Flask(__name__)

app.config['MONGO_DBNAME']='loginsys'

mongo=PyMongo(app)

@app.route('/')
def index():
	if 'username' in session:
		return redirect(url_for('mainpage'))
	return render_template('Login.html')
	
@app.route('/Login',methods=['POST'])
def Login():
	users=mongo.db.users
	user_login=users.find_one({'name':request.form['username']})
	
	if user_login:
		if bcrypt.hashpw(request.form['pass'].encode('utf-8'), user_login['password'].encode('utf-8')) == user_login['password'].encode('utf-8'):
			session['username'] = request.form['username']
			return redirect(url_for('index'))
	
	return 'Invalid Username and Password Combination'
	
	
@app.route('/Registration',methods=['POST','GET'])
def Registration():
	if request.method=='POST':
		users = mongo.db.users
		existing_user = users.find_one({'name' : request.form['username']})

		if existing_user is None:
			hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
			users.insert({'name' : request.form['username'], 'password' : hashpass})
			session['username'] = request.form['username']
			return redirect(url_for('index'))
			
		return "Username already exists"
	return render_template('Registration.html')
	
@app.route('/mainpage',methods=['POST','GET'])
def mainpage():
	return render_template('mainpage.html',success=session['username'])
	
@app.route('/Logout',methods=['POST','GET'])
def Logout():
	session.pop('username',None)
	return redirect(url_for('index'))
	
if __name__=='__main__':
	app.secret_key='anish'
	app.run(debug=True)
        
	
