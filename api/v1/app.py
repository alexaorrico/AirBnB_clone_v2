#!/usr/bin/python3
"""app Module"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(junk):
    """
    Removes current SQLAlchemy Session.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Return 404 error JSON string.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    h = environ.get('HBNB_API_HOST', '0.0.0.0')
    p = environ.get('HBNB_API_PORT', '5000')
    app.run(host=h, port=p, threaded=True)
