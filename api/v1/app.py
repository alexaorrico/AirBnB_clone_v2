#!/usr/bin/python3
"""Flask Setup"""

from models import storage
from api.v1.views import app_views
import flask
from flask import request, jsonify
from os import environ

app = flask.Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(self):
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """404 error"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    env_host = environ.get('HBNB_API_HOST', default='0.0.0.0')
    env_port = environ.get('HBNB_API_PORT', default=5000)
    app.run(host=env_host, port=int(env_port), threaded=True)
