#!/usr/bin/python3
"""Py module utilizes flask to run app"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")

app_views = Blueprint("app_views", __name__)


@app.teardown_appcontext
def tearDown(error):
    """tearDown method"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST'), port=int(getenv('HBNB_API_PORT')),
            threaded=True)
