import math
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
from financeapp.transactions import get_categories



bp = Blueprint('graph', __name__)


@bp.route('/graph')
@login_required
def index():    

    #Getting transaction data
    db = get_db()
    c = db.cursor()
    transactions = c.execute(
        'SELECT *'
        'FROM ((transactions t JOIN users u ON t.user_id = u.id)'
        'JOIN categories c ON t.category_id = c.id_categories)'        
        'where t.user_id = ?',  (g.user['id'],)
    )


    result = [dict(row) for row in transactions.fetchall()]   
        
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


    #Extracting the data and grouping it   - 2nd
    
    categories = c.execute(
        'SELECT *'
        ' FROM categories c JOIN users u ON c.user_id = u.id where c.user_id = ?',  (g.user['id'],)
    )
    
    categories_result = [dict(row) for row in categories.fetchall()]   
    #print(categories_result)


    df2 = pd.DataFrame(categories_result)
    df2.category = df2.category.astype(str)
    group_result2 = df2.groupby('category')['amount_budget'].sum()
    print(group_result2)
    source2 = ColumnDataSource(pd.DataFrame(group_result2))
    category = source2.data['category'].tolist()


    # #2nd plot
    # fig1 = figure(x_range=category, height=400, width=1100, tooltips=[("category_id", "@category_id")])
    # fig1.vbar(x='category', top='amount_budget', source=source2, width=0.9)
    # fig1.xaxis.axis_label = "Category"
    # fig1.yaxis.axis_label = "Amount"
    # fig1.legend.location = "top_left"
    # fig1.xaxis.major_label_orientation = math.pi/3
    # script2, div2 = components(fig1)


    #Extracting the data and grouping it   - 3rd    
    group_result_category = df.groupby('category')['amount'].sum()
    df3 = df2.join(group_result_category,  lsuffix='_cat', rsuffix='_tx', on='category')
    source3 = ColumnDataSource(pd.DataFrame(df3))
    category = source3.data['category'].tolist()

    f = category
    f1 = [(c, 'amount') for c in f  ]
    f2 = [(c, 'amount_budget') for c in f  ]
    factors = (f1+f2)

    #3rd plot

    # f = category
    # f1 = [(c, 'amount') for c in f  ]
    # f2 = [(c, 'amount_budget') for c in f  ]
    # factors = (f1+f2)

    fig2 = figure(x_range=category, height=400, width=1100, tooltips=[("Budget", "@amount_budget"), ("Spent", "@amount")])
    fig2.vbar(x='category', top='amount', source=source3, width=0.9, color="red")
    fig2.vbar(x='category', top='amount_budget', source=source3, width=0.9, color="green")
    fig2.xaxis.axis_label = "Category"
    fig2.yaxis.axis_label = "Amount"
    fig2.legend.location = "top_left"
    fig2.xaxis.major_label_orientation = math.pi/3
    script3, div3 = components(fig2)

    

    return render_template(
        'graph/index.html',
        script0 = script0,
        div0 = div0, 
        # script2 = script2, 
        # div2 = div2,
        script3 = script3,
        div3 = div3, 
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')