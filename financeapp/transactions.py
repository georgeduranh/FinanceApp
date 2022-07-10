from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from financeapp.auth import login_required
from financeapp.db import get_db

bp = Blueprint('transactions', __name__)


@bp.route('/')
def index():
    db = get_db()
    transactions = db.execute(
        'SELECT t.id, registered_time, date, description, is_paid, category_id, payment_method_id'
        ' FROM transactions t JOIN users u ON t.user_id = u.id'
        ' ORDER BY date DESC'
    ).fetchall()
    return render_template('transactions/index.html', transactions=transactions)

    