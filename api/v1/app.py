#!/usr/bin/python3
"""This script returns the API status """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.teardown_appcontext
def teardown(exception):
    """closes the current sqlalchemy session"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """handler for 404 error returning 404 status code in JSON-format"""
    return jsonify(error="Not found"), 404

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST') or '0.0.0.0'
    port = getenv('HBNB_API_PORT') or 5000
    app.run(host=host, port=port, threaded=True)
