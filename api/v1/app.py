#!/usr/bin/python3
"""
initializes flask app
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv
from models import storage


app = Flask(__name__)

@app.teardown_appcontext
def close_storage(exception=None):
    storage.close()

app.register_blueprint(app_views)

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_HOST:
        host = HBNB_API_HOST
    if HBNB_API_PORT:
        port = int(HBNB_API_PORT)
    app.run(host=host, port=port, threaded=True)