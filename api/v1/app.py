#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, jsonify, Blueprint, make_response
from os import getenv
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """note that we set the 404 status explicitly"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    if host is None:
        host = "0.0.0.0"
    port = getenv("HBNB_API_PORT")
    if port is None:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
