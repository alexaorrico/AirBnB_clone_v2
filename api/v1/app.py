#!/usr/bin/python3
"""
API for AirBnB Clone
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from flasgger import Swagger
from flask_cors import (CORS, cross_origin)
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, origins="0.0.0.0")
Swagger(app)

@app.teardown_appcontext
def teardown_db(exception):
    """close the storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"errors": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)

