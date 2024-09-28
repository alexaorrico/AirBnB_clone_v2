#!/usr/bin/python3
"""
    This Module Contains the api using flask
"""
from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(blueprint=app_views)


@app.route('/')
def home():
    return "Home"


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close(exception=True):
    return storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST")
    HBNB_API_PORT = getenv("HBNB_API_PORT")
    if not getenv("HBNB_API_HOST"):
        HBNB_API_HOST = '0.0.0.0'
    if not getenv("HBNB_API_PORT"):
        HBNB_API_PORT = '5000'
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
