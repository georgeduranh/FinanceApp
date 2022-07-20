from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('categories', __name__)


@bp.route('/categories')
def index_cat():
    db = get_db()
    categories = db.execute(
        'SELECT *'
        ' FROM categories'
    ).fetchall()
    
    return render_template('categories/index.html', categories=categories)
