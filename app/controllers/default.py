import bcrypt
from app import app
from app.models.tables import User
from bottle import template, static_file, request, redirect

# static routes
@app.get('/<filename:re:.*\.css>')
def stylesheet(filename):
	return static_file(filename, root='app/static/css')

@app.get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='app/static/js')

@app.get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='app/static/img')

@app.route('/register')
def do_register():
	return template('register', username_exists=False, email_exists=False)

@app.route('/register', method='POST')
def do_register(db, session):
	username = request.forms.get('username')
	email = request.forms.get('email')
	password = request.forms.get('password')
	confirm_password = request.forms.get('confirm-password')
	
	if db.query(User).filter(User.email==email).one_or_none():
		return template('register', email_exists=True, username_exists=False)

	if db.query(User).filter(User.username==username).one_or_none():
		return template('register', email_exists=False, username_exists=True)

	password = password.encode()
	hashed = bcrypt.hashpw(password, bcrypt.gensalt())

	new_user = User(username, email, hashed)
	db.add(new_user)
	session['name'] = email
	return redirect('home')

@app.route('/') # @get('/login')
def login():
	return template('login', email_ok=True, password_ok=True)

@app.route('/', method='POST') # @post('/login')
def do_login(db, session):
	email = request.forms.get('email')
	password = request.forms.get('password')

	try:
		user = db.query(User).filter(User.email==email).one()
	except:
		return template('login', email_ok=False, password_ok=True)

	if bcrypt.checkpw(password.encode(), user.password):
		session['name'] = email
		return redirect('home')
	else:
		return template('login', email_ok=True, password_ok=False, email=email)

@app.route('/home')
def do_register(db, session):
	if not session.get('name'):
		return template('login', email_ok=True, password_ok=True)
	return template('home')

@app.error(404)
def error404(error):
	return template('page_not_found')
