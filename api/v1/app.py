#!/usr/bin/python3
"""a module containing flask app functions"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
host = getenv('HBNB_API_HOST') or '0.0.0.0'
port = getenv('HBNB_API_PORT') or '5000'

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """handles app teardown by closing database session"""
    storage.close()


@app.errorhandler(404)
def error_not_found(error):
    """handles page not found error by loading a custom json object"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port)
