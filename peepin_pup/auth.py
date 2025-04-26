import os
import functools
from flask import( Blueprint, flash, g, redirect, render_template, request, session, url_for
    )
from werkzeug.security import check_password_hash, generate_password_hash
from peepin_pup.db import get_db, query_db, insert_db
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        secret_value = os.environ.get('SECRET')
        username = request.form['username']
        password = request.form['password']
        secret = request.form['secret']
        db = get_db()
        error = None

        if not username or not password or not secret or secret != secret_value:
            error = 'FAIL. Try again'

        if error is None:
            try:
                insert_db(
                    "INSERT INTO user_id (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password))
                )
            except db.IntegrityError:
                error = "Registration Failed"
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = query_db(
            'SELECT * FROM user_id WHERE username = %s', (username,), one=True
        )
        if user is None:
            error = 'Login Incorrect'
        elif not check_password_hash(user['password'], password):
            error = 'Login Incorrect'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))

        flash(error)
    
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = query_db(
                'SELECT * FROM user_id WHERE id = %s', (user_id,), one=True
        )

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
