#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.config['DEBUG'] = True
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """
    method to close the storage after each request
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a JSON-formatted 404 status error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
