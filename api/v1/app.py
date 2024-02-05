#!/usr/bin/python3
"""Create a flask application for the API"""

from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(eexception):
    """Closes the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    '''Returns the JSON {"error": "Not found"} if resource wasn't found'''
    return jsonify({"error": "Not found"}), e.code


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=getenv("HBNB_API_PORT", '5000'),
            threaded=True)
