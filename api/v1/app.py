#!/usr/bin/python3
""" Api module """
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import json
import os

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exception):
    """teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """page not founnd error"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    env_host = 'HBNB_API_HOST'
    env_port = 'HBNB_API_PORT'
    host = os.getenv(env_host, default='0.0.0.0')
    port = os.getenv(env_port, default=5000)
    app.run(host=host, port=port, threaded=True)
