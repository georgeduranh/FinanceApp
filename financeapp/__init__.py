import os
from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'financeapp.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    ## Define DB
    from . import db
    db.init_app(app)

    ## Login view
    from . import auth
    app.register_blueprint(auth.bp)


    #Transactions view
    from . import transactions
    app.register_blueprint(transactions.bp)
    app.add_url_rule('/', endpoint='index')

    #Transactions view
    from . import categories
    app.register_blueprint(categories.bp)
    app.add_url_rule('/categories', endpoint='index')

    #Transactions view
    from . import payment_methods
    app.register_blueprint(payment_methods.bp)
    app.add_url_rule('/payment_methods', endpoint='index')

     #Transactions view
    from . import transaction_types
    app.register_blueprint(transaction_types.bp)
    app.add_url_rule('/transaction_types', endpoint='index')

    return app