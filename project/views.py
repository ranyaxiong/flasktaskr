import sqlite3
from functools import wraps
from flask import Flask, flash, redirect, request, render_template, url_for,session

# config
app = Flask(__name__)
app.config.from_object('_config')

# helper functions
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def loing_required(test):
    @wraps
    def wrap(*args, **kargs):
        if 'logged_in' in session:
            return test(*args, **kargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

# route handlers
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(url_for('login'))

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid Credentials, Please try again.'
            return render_template("login.html", error=error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('tasks'))
    return render_template('login.html')