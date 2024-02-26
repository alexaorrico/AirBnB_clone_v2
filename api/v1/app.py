#!/usr/bin/python3
"""
Your first endpoint (route) will be to return the status of your API:
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
# from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown(exc):
    """removes the current sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """handles 404 errors"""
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    """runs the api using  environment variables"""
    app.run(host=os.environ.get('HBNB_API_HOST'),
            port=os.environ.get('HBNB_API_PORT'))
