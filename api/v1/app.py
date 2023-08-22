#!/usr/bin/python3
"""app.py module"""
from api.v1.app import app_views
from flask import Flask, Blueprint
from models import storage
from os import getenv

app = Flask(__name__)

# Not sure if this is correct
app_views = Blueprint("app_views", __name__, template_folder="templates")


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),  # 0.0.0.0 if no env set
        port=getenv("HBNB_API_PORT", 5000),
        threaded=True,
    )
