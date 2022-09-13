import pandas as pd 

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from easybase import get
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

from financeapp.auth import login_required
from financeapp.db import get_db



bp = Blueprint('graph', __name__)


@bp.route('/graph')
@login_required
def index():    

    #Getting transaction data
    db = get_db()
    c = db.cursor()
    categories = c.execute(
        'SELECT *'
        ' FROM transactions t JOIN users u ON t.user_id = u.id where t.user_id = ?',  (g.user['id'],)
    )

    result = [dict(row) for row in categories.fetchall()]   
        
    # example: https://betterprogramming.pub/deploy-interactive-real-time-data-visualizations-on-flask-with-bokeh-311239273838 

    #Extracting the data and grouping it 
    df = pd.DataFrame(result)
    df.date_tx = df.date_tx.astype(str)
    group_result = df.groupby('date_tx')['amount'].sum()
    print(group_result)
    source = ColumnDataSource(pd.DataFrame(group_result))
    date_tx = source.data['date_tx'].tolist()

    #1st plot 
    fig = figure(x_range=date_tx, height=400, tooltips=[("category_id", "@category_id")])
    fig.vbar(x='date_tx', top='amount', source=source, width=0.9)
    fig.xaxis.axis_label = "Date"
    fig.yaxis.axis_label = "Amount"
    fig.legend.location = "top_left"
    script0, div0 = components(fig)


    #2nd plot
    fig1 = figure(x_range=date_tx, height=400, tooltips=[("category_id", "@category_id")])
    fig1.vbar(x='date_tx', top='amount', source=source, width=0.9)
    fig1.xaxis.axis_label = "Date"
    fig1.yaxis.axis_label = "Amount"
    fig1.legend.location = "top_left"
    script2, div2 = components(fig)
    column(fig,fig1)


    return render_template(
        'graph/index.html',
        script0 = script0,
        div0 = div0, 
        script2 = script2, 
        div2 = div2,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')