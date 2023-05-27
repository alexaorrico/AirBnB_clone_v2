#!/usr/bin/python3
"""
Module contains all API routes for the AirBnB clone project
"""


from os import getenv
from models import storage
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """
    Closes all sessions running in storage
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
    Handles the 404 error
    """
    status = {"error": "Not found"}
    return jsonify(status), 404


@app.errorhandler(404)
def not_found(error):
    """Handles the 404 error"""
    return make_response(jsonify({'error': 'Not Found'}), 404)


if __name__ == '__main__':
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),
        port=int(getenv("HBNB_API_PORT", "5000")),
        threaded=True
    )
