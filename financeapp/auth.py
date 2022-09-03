import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from financeapp.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        last_name = request.form['last_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        default_categories = ["Mercado", "Domicilio", "Transporte", "Comida fuera", "Ropa" , "Viajes", "Compras Casa", "Entretenimiento", "Donacion", "Gasto laboral",
                                "Impuestos", "Arriendo", "Servicios", "Pago tarjeta", "Salud personal", "Medicina", "Educacion", "Detalles", "Celular", "Gastos financieros", 
                                "Suscripciones", "Seguridad social","Inversion", "Prestamo", "AFC", "Pension", "Fondo Emergencia", "Ahorros viajes", "Ahorros navidad", "Ahorros cumple"]

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (name, last_name, email, login, password) VALUES (?, ?, ?, ?, ?)",
                    (name, last_name, email, username,
                     generate_password_hash(password)),
                )
                db.commit()
                

                user = db.execute(
                    'SELECT id FROM users WHERE login = ?', (username,)
                ).fetchone()
                
                user = user['id']
                amount_budget = 0.0

                
                for category in default_categories:
                    db.execute(
                        "INSERT INTO categories (category, user_id, amount_budget) VALUES (?, ?, ?)",
                        (category, user, amount_budget),
                    )
                    db.commit()


                


            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE login = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


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
