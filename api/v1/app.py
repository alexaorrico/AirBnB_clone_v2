#!/usr/bin/python3
"""Module that run the server"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)


cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.do_teardown_appcontext
def do_teardownZ(exception):
    """method that close the session """
    storage.close()


@app.errorhandler(404)
def json_not_found(exception):
    """function that handles 404 error"""
    return make_response(jsonify({"error": "Not Found"}), 404)


if __name__ == '__main__':
    """host and port"""
    app.run(host='0.0.0.0', port=5000)
