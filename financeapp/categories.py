from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('categories', __name__)


@bp.route('/categories', )
@login_required
def index_cat():
    db = get_db()
    categories = db.execute(
        'SELECT *'
        ' FROM categories c JOIN users u ON c.user_id = u.id where c.user_id = ?',  (g.user['id'],)
    ).fetchall()
    
    return render_template('categories/index.html', categories=categories)


@bp.route('/categories/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':        
        category = request.form['category']   
        amount_budget = request.form['amount_budget']   
       
        error = None

        if not category:
            error = 'category is required.'      


        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO categories (category, user_id, amount_budget) VALUES (?, ?, ?)",
                ( category, g.user['id'], amount_budget),
            )
            db.commit()
            return redirect(url_for('categories.index_cat'))

    return render_template('categories/create.html')

def get_cat(id, check_author=True):
    category = get_db().execute(
        'SELECT *'
        ' FROM categories c JOIN users u ON c.user_id = u.id'
        ' WHERE c.id_categories = ?',
        (id,)
    ).fetchone()

    if category is None:
        abort(404, f"Categorty id {id} doesn't exist.")

    if category['user_id'] != g.user['id']:
        abort(403)

    return category

@bp.route('/categories/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    category = get_cat(id)
    error = None

    if request.method == 'POST':
        category = request.form['category']   
        amount_budget = request.form['amount_budget']   
           

        if not category:
            error = 'Category is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE categories SET category = ?,  amount_budget = ?'
                ' WHERE id_categories = ?',
                ( category, amount_budget, id)
            )
            db.commit()
            return redirect(url_for('categories.index_cat'))

    return render_template('categories/update.html', category=category)

@bp.route('/categories/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_cat(id)
    db = get_db()
    db.execute('DELETE FROM categories WHERE id_categories = ?', (id,))
    db.commit()
    return redirect(url_for('categories.index_cat'))

