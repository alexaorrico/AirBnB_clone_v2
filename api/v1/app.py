#!/usr/bin/python3
"""immported modules pa"""
import os
from api.v1.views import app_views
from models import storage
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """close the storage instance"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """404 not found"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', default="0.0.0.0")
    port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)
