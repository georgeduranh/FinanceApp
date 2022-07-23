from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('transaction_types', __name__)


@bp.route('/transaction_types', )
@login_required
def index_transaction_type():
    db = get_db()
    transaction_types = db.execute(
        'SELECT *'
        ' FROM transaction_types c JOIN users u ON c.user_id = u.id where c.user_id = ?',  (g.user['id'],)
    ).fetchall()
    
    return render_template('transaction_types/index.html', transaction_types=transaction_types)


@bp.route('/transaction_types/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':        
        transaction_type = request.form['transaction_type']   
       
        error = None

        if not transaction_type:
            error = 'transaction_type is required.'      


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO transaction_types (transaction_type, user_id) VALUES (?, ?)",
                ( transaction_type, g.user['id'],),
            )
            db.commit()
            return redirect(url_for('transaction_types.index_transaction_type'))

    return render_template('transaction_types/create.html')

def get_tt(id, check_author=True):
    transaction_type = get_db().execute(
        'SELECT *'
        ' FROM transaction_types c JOIN users u ON c.user_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if transaction_type is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    if transaction_type['user_id'] != g.user['id']:
        abort(403)

    return transaction_type

@bp.route('/transaction_types/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    transaction_type = get_tt(id)
    error = None

    if request.method == 'POST':
        transaction_type = request.form['transaction_type']      

        if not transaction_type:
            error = 'transaction_type is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE transaction_types SET transaction_type = ?'
                ' WHERE id = ?',
                ( transaction_type, id)
            )
            db.commit()
            return redirect(url_for('transaction_types.index_transaction_type'))

    return render_template('transaction_types/update.html', transaction_type=transaction_type)

@bp.route('/transaction_types/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_tt(id)
    db = get_db()
    db.execute('DELETE FROM transaction_types WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('transaction_types.index_transaction_type'))

