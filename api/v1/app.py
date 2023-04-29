#!/usr/bin/python3
"""A Script that return the status of API"""
import os
from flask import Flask
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import HTTPException
from models import storage
from app.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resouces={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown(exc):
    """Function that closes the current session"""
    storage.close()


@app.error_handler(404)
def error_handler():
    """A route that handles 404 (not found) error"""
    return jsonify({"error": "Not found"})


if __name__ == '__main__':
    app.run(host=host, port=port debug=True)
