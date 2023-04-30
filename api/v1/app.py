#!/usr/bin/python3
"""
starts a Flask web application
"""

from os import getenv

from flask import Flask, jsonify
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """custom page not found error"""
    return jsonify(error="Not found"), 404


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")

    app.run(
        host=host if host is not None else '0.0.0.0',
        port=port if port is not None else '5000',
        threaded=True,
    )
