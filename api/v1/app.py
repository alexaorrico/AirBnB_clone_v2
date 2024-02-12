#!/usr/bin/python3
"""this module is the start of my api"""
from models import storage
from .views import app_views
from flask import Flask
from os import getenv

# create a variable named app instance of flask
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(err):
    """a method to handle @app.teardown_appcontext"""
    storage.close()



def app_run():
    """a method that runs the flask server variable (app)"""
    try:
        host_ = getenv(HBNB_API_HOST)
    except Exception:
        host_ = "0.0.0.0"
    try:
        port_ = getenv(HBNB_API_PORT)
    except Exception:
        port_ = "5000"
    app.run(host=host_, port=port_, threaded=True)


if __name__ == "__main__":
    app_run()
