from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .auth import auth
#from .models import UserModel

##https://flask-login.readthedocs.io/en/latest/ 
login_manager = LoginManager()

@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    #configuración de la app  
    app.config.from_object(Config)
    app.register_blueprint(auth)
    login_manager.init_app(app)

    return app

login_manager.login_view = 'auth.login'