from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('categories', __name__)


@bp.route('/categories')
@login_required
def index_cat():
    db = get_db()
    categories = db.execute(
        'SELECT *'
        ' FROM categories c JOIN users u ON c.user_id = u.id'
    ).fetchall()
    
    return render_template('categories/index.html', categories=categories)


@bp.route('/categories/create', methods=('GET', 'POST'))
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
                "INSERT INTO categories (category, user_id) VALUES (?, ?)",
                ( category, g.user['id'],),
            )
            db.commit()
            return redirect(url_for('categories.index_cat'))

    return render_template('categories/create.html')

