#!/usr/bin/python3
""" a Flask app"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(self):
    """closes storage if it exist"""
    if Storage is not None:
        storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """error message for page not found"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', '5000'),
            threaded=True)
