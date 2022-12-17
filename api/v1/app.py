#!/usr/bin/python3
"""starts a Flask web application"""

from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask
from flask_cors import CORS
from flask import jsonify


app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(self):
    """close a session"""
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    HBNB_API_HOST = '0.0.0.0'
    HBNB_API_PORT = '5000'
    if getenv('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if getenv('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=port, threaded=True)
