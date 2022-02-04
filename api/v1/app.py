#!/usr/bin/python3
"""
Script that starts a Flask web application
"""
from flask import Flask, Response, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear(self):
    """Method to handle tearmod"""
    storage.close()


@app.errorhandler(404)
def error_message(e):
    """ Return JSON file error message """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":

    HBNB_API_HOST = getenv("HBNB_API_HOST") or "0.0.0.0"

    HBNB_API_PORT = getenv("HBNB_API_PORT") or 5000

    app.run(host=HBNB_API_HOST, port=int(
        HBNB_API_PORT), threaded=True)
