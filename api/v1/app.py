#!/usr/bin/python3
"""This will return the status code"""
from flask import Flask
from flask import jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(ctx):
    """To remove the current SQL Alchemy"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Method that returns 404 error using JSON"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
