#!/usr/bin/python3
"""Contains app-flask and endpoints (routes)"""
from flask import Flask, Blueprint, abort
from flask import render_template, jsonify
from flask import make_response
from flask_cors import CORS
import os
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def invalid_route(e):
    return (jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def storage_close(issue):
    """calls storage.close()"""
    storage.close()


if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True, debug=True)
