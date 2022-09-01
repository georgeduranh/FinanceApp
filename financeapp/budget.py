from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('budget', __name__)


@bp.route('/budget', )
@login_required
def index_budget():
    db = get_db()
    budget = db.execute(
        'SELECT *'
        ' FROM budget c JOIN users u ON c.user_id = u.id'
        ' JOIN categories cat ON cat.user_id = u.id where  c.user_id = ? ',  (g.user['id'],)
    ).fetchall()
    
    return render_template('budget/index.html', budget=budget)


@bp.route('/budget/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':        
        category = request.form['category'] 
        
       
        error = None

        if not category:
            error = 'category is required.'      


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO budget (category_id, user_id) VALUES (?, ?)",
                ( category_id, g.user['id'],),
            )
            db.commit()
            return redirect(url_for('budget.index_budget'))

    return render_template('budget/create.html')

def get_cat(id, check_author=True):
    category = get_db().execute(
        'SELECT *'
        ' FROM budget c JOIN users u ON c.user_id = u.id'
        ' WHERE c.id_budget = ?',
        (id,)
    ).fetchone()

    if category is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    if category['user_id'] != g.user['id']:
        abort(403)

    return category

@bp.route('/budget/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    category = get_cat(id)
    error = None

    if request.method == 'POST':
        category = request.form['category']      

        if not category:
            error = 'Category is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE budget SET category = ?'
                ' WHERE id_budget = ?',
                ( category, id)
            )
            db.commit()
            return redirect(url_for('budget.index_budget'))

    return render_template('budget/update.html', category=category)

@bp.route('/budget/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_cat(id)
    db = get_db()
    db.execute('DELETE FROM budget WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('budget.index_budget'))