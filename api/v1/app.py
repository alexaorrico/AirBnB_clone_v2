#!/usr/bin/python3
"""
A python script that starts a Flask web application
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception=None):
    """
     Function closes the current session
    """
    storage.close()


if __name__ == '__main__':
    h = getenv('HBNB_API_HOST')
    p = getenv('HBNB_API_PORT')
    app.run(host=h, port=p, threaded=True)