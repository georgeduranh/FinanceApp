from datetime import datetime
from datetime import date

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
    categories = get_categories()
    payment_methods =  get_payment_methods()
    transaction_types =  get_transaction_types()

    transactions = db.execute(
        'SELECT t.id, t.registered_time, t.user_id, t.description, t.amount, t.date_tx, t.is_paid, category_id, payment_method_id, type_id'
        ' FROM transactions t JOIN users u ON t.user_id = u.id Where t.user_id = ?'
        
        ' ORDER BY registered_time DESC', (g.user['id'],)
    ).fetchall()
    
    return render_template('transactions/index.html', transactions=transactions, categories=categories, payment_methods=payment_methods, transaction_types=transaction_types)



def get_categories(check_author=True):
    categories = get_db().execute(
        'SELECT *'
        ' FROM categories c JOIN users u ON c.user_id = u.id where c.user_id = ?',  (g.user['id'],)
    ).fetchall()

    if categories is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    return categories

def get_payment_methods(check_author=True):
    payment_methods = get_db().execute(
        'SELECT *'
        ' FROM payment_methods c JOIN users u ON c.user_id = u.id where c.user_id = ?',  (g.user['id'],)
    ).fetchall()

    if payment_methods is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    return payment_methods


def get_transaction_types(check_author=True):
    transaction_types = get_db().execute(
        'SELECT *'
        ' FROM transaction_types c JOIN users u ON c.user_id = u.id where c.user_id = ?',  (g.user['id'],)
    ).fetchall()

    if transaction_types is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    return transaction_types



@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    categories = get_categories()
    payment_methods =  get_payment_methods()
    transaction_types =  get_transaction_types()
    
    # mm/dd/y
    today = date.today()
    default_date = today.strftime("%m/%d/%Y")
    #print(default_date)
    


    if request.method == 'POST':
        date_tx = request.form['date_tx']
        description = request.form['description']
        is_paid = request.form['is_paid']
        category_id = request.form['category_id']
        payment_method_id = request.form['payment_method_id']
        type_id = request.form['type_id']
        amount = request.form['amount']
        
        
        error = None

        if not date_tx:
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
                ( date_tx, description, is_paid, category_id, payment_method_id, g.user['id'], type_id, amount),
            )
            db.commit()
            return redirect(url_for('transactions.index'))

    return render_template('transactions/create.html', categories=categories, payment_methods=payment_methods, transaction_types=transaction_types, default_date=default_date)


def get_tx(id, check_author=True):
    transaction = get_db().execute(
        'SELECT t.id, description, user_id, amount, date_tx, category_id, payment_method_id, is_paid, type_id '
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
    payment_methods =  get_payment_methods()
    transaction_types =  get_transaction_types()

    if request.method == 'POST':
        description = request.form['description']
        date = request.form['date']
        amount = request.form['amount']
        payment_method_id  = request.form['payment_method_id']
        category_id = request.form['category_id']
        type_id = request.form['type_id']
        is_paid = request.form['is_paid']

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
                'UPDATE transactions SET description = ?, date_tx = ?, amount=?, payment_method_id=?, category_id=?, type_id=?, is_paid=?'
                ' WHERE id = ?',
                ( description, date, amount, payment_method_id, category_id, type_id, is_paid,  id)
            )
            db.commit()
            return redirect(url_for('transactions.index'))

    return render_template('transactions/update.html', transaction=transaction, categories=categories, payment_methods=payment_methods, transaction_types=transaction_types)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_tx(id)
    db = get_db()
    db.execute('DELETE FROM transactions WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('transactions.index'))