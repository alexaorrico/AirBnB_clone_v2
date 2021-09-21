#!/usr/bin/python3
"""Module for API"""
from api.v1.views import app_views
from flask import Blueprint, Flask, jsonify, make_response
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """handles teardown_appcontext"""
    storage.close()

@app.errorhandler(404)
def page_not_found(error):
    """handler for 404 errors JSON format"""
    return make_response(jsonify({"erorr": "Not found"}), 404)

if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host, port, threaded=True)
