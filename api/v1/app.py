#!/usr/bin/python3
"""app.py module"""
from api.v1.views import app_views
from flask import Flask, Blueprint
from models import storage
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return {"error": "Not found"}


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),  # 0.0.0.0 if no env set
        port=getenv("HBNB_API_PORT", 5000),
        threaded=True,
    )
