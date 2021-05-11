#!/usr/bin/python3
"""
Airbnb clone application implementation using flask
"""
from flask import Flask, jsonify, make_response, Blueprint
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(code):
    """Calls storage.close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Displays json string in the evnt of a 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(getenv('HBNB_API_PORT', '5000')),
            threaded=True,
            debug=True)
