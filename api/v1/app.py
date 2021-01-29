#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Flask, render_template, Blueprint, jsonify
from flask_cors import CORS
from models import storage
import os
from api.v1.views import app_views
app = Flask(__name__)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_api(exception):
    """After query return ends current session"""
    return storage.close()


@app.errorhandler(404)
def not_found(exception):
    """Handles page not found error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = int(os.getenv('HBNB_API_PORT'))

    """ os.environ['HBNB_API_HOST'] = '0.0.0.0'
    host = '0.0.0.0'
    os.environ['HBNB_API_PORT'] = '5000'
    port = '5000'"""

    app.run(host=host, port=port, threaded=True)
