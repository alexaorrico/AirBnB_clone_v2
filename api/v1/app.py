#!/usr/bin/python3
"""Script that starts a Flask API"""
from models import storage
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, request
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown_db(self):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def handle_404(e):
    """error 404"""
    return (jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
