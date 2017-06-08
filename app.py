from bottle import route, run
from bottle import request, template
from bottle import static_file, get
from bottle import error
import os

@get('/<filename:re:.*\.css>')
def stylesheet(filename):
	return static_file(filename, root='static/css')

@get('/<filename:re:.*\.js>')
def javascripts(filename):
	return static_file(filename, root='static/js')

@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
	return static_file(filename, root='static/img')

@route('/') # @get('/login')
def login():
	return template('login')

def check_login(email, password):
	d = {'atilla@gmail.com':'python', 'jobs@gmail.com':'apple', 'gates@gmail.com':'microsoft'}
	if email in d.keys() and d[email] == password:
		return True
	return False

@route('/', method='POST') # @post('/login')
def do_login():
	email = request.forms.get('email')
	password = request.forms.get('password')
	return template('verify_login', sucess=check_login(email, password))

@route('/register')
def do_register():
	return template('register')

def check_register(email, password, confirm_password):
	d = {'atilla':'atilla@gmail.com', 'jobs':'jobs@gmail.com', 'gates':'gates@gmail.com'}
	if email in d.values():
		return 0
	elif password != confirm_password:
		return -1
	else:
		return 1

@route('/register', method='POST')
def do_register():
	username = request.forms.get('username')
	email = request.forms.get('email')
	password = request.forms.get('password')
	confirm_password = request.forms.get('confirm-password')
	return template('verify_register', sucess=check_register(email, password, confirm_password))

@error(404)
def error404(error):
	return template('page_not_found')

if __name__ == '__main__':
	if os.environ.get('APP_LOCATION') == 'heroku':
		run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
	else:
		run(host='localhost', port=8080, debug=True, reloader=True)