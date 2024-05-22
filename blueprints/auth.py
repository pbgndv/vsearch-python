from flask import Blueprint, request, session, redirect, url_for, render_template
from functools import wraps

auth_bp = Blueprint('auth', __name__)

users = {
    'admin': 'password',
    'letrider': 'pass'
}

def check_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        return redirect(url_for('auth.login'))
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username in users and users[username] == password:
                session['logged_in'] = True
                return redirect(url_for('views.view_log'))
            else:
                return 'Invalid credentials', 401
        return '''
            <form method="post">
                <p><input type=text name=username placeholder=username>
                <p><input type=password name=password placeholder=password>
                <p><input type=submit value=Login>
            </form>
        '''
    except Exception as e:
        return f"An error occurred during login: {e}", 500

@auth_bp.route('/logout')
def logout():
    try:
        session.pop('logged_in', None)
        return 'You are now logged out'
    except Exception as e:
        return f"An error occurred during logout: {e}", 500

@auth_bp.route('/status')
def status():
    try:
        if 'logged_in' in session and session['logged_in']:
            return 'You are logged in'
        return 'You are not logged in'
    except Exception as e:
        return f"An error occurred while checking status: {e}", 500
