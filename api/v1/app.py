#!/usr/bin/python3
"""Create a flask application for the API"""

from os import getenv

from flask import Flask, jsonify

from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(eexception):
    """Closes the storage"""
    storage.close()

from flask import jsonify
@app.errorhandler(404)
def error_handler_404(error):
    '''Returns the JSON {"error": "Not found"} if resource wasn't found'''
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", '0.0.0.0'),
            port=getenv("HBNB_API_PORT", '5000'),
            threaded=True)
