#!/usr/bin/python3
"""app.py to connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()

@app.errorhandler(404)
def error_handler(error):
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))