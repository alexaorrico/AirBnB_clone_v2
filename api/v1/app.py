#!/usr/bin/python3
"""The app module"""
from flask import Flask, jsonify, make_response, request, abort
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv
HOST = getenv("HBNB_API_HOST") or '0.0.0.0'
PORT = getenv("HBNB_API_PORT") or '5000'

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': HOST}})


@app.teardown_appcontext
def teardown_appcontext(code):
    """Close storage in when flask app finish its process"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Handle 404 not found page"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.before_request
def check_content_type():
    """Check if the request content type is not JSON"""
    if request.content_type and request.content_type != 'application/json':
        abort(400, description="Content-Type must be application/json")


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
