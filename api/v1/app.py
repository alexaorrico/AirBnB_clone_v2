#!/usr/bin/python3
"""
Setups variable app
"""

from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources=r'/*', origins=['0.0.0.0'])

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ Closes current SQLAlchemy session"""
    return storage.close()


@app.errorhandler(404)
def error(e):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else 5000
    app.run(host=host, port=port, threaded=True)
