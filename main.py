import os


#from app
from financeapp import create_app

appid = os.environ.get('ACCESS_KEY')

app = create_app()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"