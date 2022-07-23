from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('payment_methods', __name__)


@bp.route('/payment_methods', )
@login_required
def index_payment_method():
    db = get_db()
    payment_methods = db.execute(
        'SELECT *'
        ' FROM payment_methods c JOIN users u ON c.user_id = u.id'
    ).fetchall()
    
    return render_template('payment_methods/index.html', payment_methods=payment_methods)


@bp.route('/payment_methods/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':        
        payment_method = request.form['payment_method']   
       
        error = None

        if not payment_method:
            error = 'payment_method is required.'      


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO payment_methods (payment_method, user_id) VALUES (?, ?)",
                ( payment_method, g.user['id'],),
            )
            db.commit()
            return redirect(url_for('payment_methods.index_payment_method'))

    return render_template('payment_methods/create.html')

def get_pm(id, check_author=True):
    payment_method = get_db().execute(
        'SELECT *'
        ' FROM payment_methods c JOIN users u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if payment_method is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    if payment_method['user_id'] != g.user['id']:
        abort(403)

    return payment_method

@bp.route('/payment_methods/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    payment_method = get_pm(id)
    error = None

    if request.method == 'POST':
        payment_method = request.form['payment_method']      

        if not payment_method:
            error = 'payment_method is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE payment_methods SET payment_method = ?'
                ' WHERE id = ?',
                ( payment_method, id)
            )
            db.commit()
            return redirect(url_for('payment_methods.index_payment_method'))

    return render_template('payment_methods/update.html', payment_method=payment_method)

@bp.route('/payment_methods/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_pm(id)
    db = get_db()
    db.execute('DELETE FROM payment_methods WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('payment_methods.index_payment_method'))

