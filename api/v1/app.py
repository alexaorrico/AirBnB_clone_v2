#!/usr/bin/python3
"""Integrates with AirBnB static HTML Template"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors that returns JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    from os import getenv
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
