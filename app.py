from flask import Flask, request, session, redirect, url_for, jsonify, render_template
from functools import wraps
from vsearch import search4letters, search4vowels
import dbconfig
import DBcm

app = Flask(__name__)
app.secret_key = 'supersecretkeyxproject'

db = DBcm.MySQLDatabase(dbconfig.db_config)

users = {
    'admin': 'password',
    'letrider': 'pass'
}

# decorators
def check_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        return redirect(url_for('login'))
    return decorated_function

# - Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if username in users and users[username] == password:
                session['logged_in'] = True
                return redirect(url_for('view_log'))
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

@app.route('/')
def home():
    try:
        return render_template('home.html')
    except Exception as e:
        return f"An error occurred: {e}", 500

@app.route('/logout')
def logout():
    try:
        session.pop('logged_in', None)
        return 'You are now logged out'
    except Exception as e:
        return f"An error occurred during logout: {e}", 500

@app.route('/status')
def status():
    try:
        if 'logged_in' in session and session['logged_in']:
            return 'You are logged in'
        return 'You are not logged in'
    except Exception as e:
        return f"An error occurred while checking status: {e}", 500

@app.route("/viewlog", methods=["GET"])
@check_logged_in
def view_log():
    try:
        logs = db.fetch_logs()
        log_list = [{"id": row[0], "message": row[1], "timestamp": row[2]} for row in logs]
        return jsonify(log_list)
    except Exception as e:
        return f"An error occurred while fetching logs: {e}", 500

@app.route('/vsearch', methods=['POST'])
def do_search():
    phrase = request.form['phrase']
    letters = request.form.get('letters', 'aeiou')
    vowels = search4vowels(phrase)
    letters_found = search4letters(phrase, letters)
    return render_template('results.html',
                           the_title='Results',
                           the_phrase=phrase,
                           the_letters=letters,
                           the_vowels=vowels,
                           the_letters_found=letters_found)

@app.route("/users", methods=["GET"])
@check_logged_in
def show_users():
    try:
        return render_template('users.html', users=users.keys())
    except Exception as e:
        return f"An error occurred while rendering the user list: {e}", 500



if __name__ == "__main__":
    app.run(debug=True)
