#!/usr/bin/python3
""" This is the app folder"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_close(self):
    """ Method to close """
    storage.close()


@app.errorhandler(404)
def error_not_found(self):
    """Method no found page"""
    return make_response(jsonify({"error": "Not found"})), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", 5000),
            threaded=True, debug=True)
