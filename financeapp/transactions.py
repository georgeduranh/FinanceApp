from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db


bp = Blueprint('transactions', __name__)

## registered_time, date, description, is_paid, category_id, payment_method_id
@bp.route('/')
@login_required
def index():
    db = get_db()
    transactions = db.execute(
        'SELECT t.id, t.registered_time, t.user_id, t.description, t.amount, t.date_tx'
        ' FROM transactions t JOIN users u ON t.user_id = u.id'
        ' ORDER BY registered_time DESC'
    ).fetchall()
    
    return render_template('transactions/index.html', transactions=transactions)



def get_categories(check_author=True):
    categories = get_db().execute(
        'SELECT *'
        ' FROM categories c JOIN users u ON c.user_id = u.id'
    ).fetchall()

    if categories is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    return categories



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    categories = get_categories()


    if request.method == 'POST':
        date = request.form['date']
        description = request.form['description']
        is_paid = request.form['is_paid']
        category_id = request.form['category_id']
        payment_method_id = request.form['payment_method_id']
        type_id = request.form['type_id']
        amount = request.form['amount']
        
        
        error = None

        if not date:
            error = 'date is required.'

        if not description:
            error = 'description is required.'
    
        if not category_id:
            error = 'category_id is required.'

        if not payment_method_id:
            error = 'payment_method_id is required.'

        if not type_id:
            error = 'type_id is required.'

        
        # Getting the current date and time
        dt = datetime.now()

        # getting the timestamp
        registered_time = datetime.timestamp(dt)        


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO transactions (date_tx, description, is_paid, category_id, payment_method_id, user_id, type_id, amount) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                ( date, description, is_paid, category_id, payment_method_id, g.user['id'], type_id, amount),
            )
            db.commit()
            return redirect(url_for('transactions.index'))

    return render_template('transactions/create.html', categories=categories)


def get_tx(id, check_author=True):
    transaction = get_db().execute(
        'SELECT t.id, description, user_id, amount, date_tx, category_id'
        ' FROM transactions t JOIN users u ON t.user_id = u.id'
        ' WHERE t.id = ?',
        (id,)
    ).fetchone()

    if transaction is None:
        abort(404, f"Transactions id {id} doesn't exist.")

    if transaction['user_id'] != g.user['id']:
        abort(403)

    return transaction

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    transaction = get_tx(id)
    categories = get_categories()

    if request.method == 'POST':
        description = request.form['description']
        date = request.form['date']
        amount = request.form['amount']
        error = None

        if not description:
            error = 'description is required.'

        if not date:
            error = 'date is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE transactions SET description = ?, date_tx = ?, amount=?'
                ' WHERE id = ?',
                ( description, date, amount, id)
            )
            db.commit()
            return redirect(url_for('transactions.index'))

    return render_template('transactions/update.html', transaction=transaction, categories=categories)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_tx(id)
    db = get_db()
    db.execute('DELETE FROM transactions WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('transactions.index'))