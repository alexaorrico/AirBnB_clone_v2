#!/usr/bin/python3
"""The Flask application module"""
from flask import Flask
from flask import jsonify
from flask import make_response
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.errorhandler(404)
def not_found(error):
    """
    Handler that returns a JSON-formatted 404 status code response.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_storage(exc):
    """Method to close the storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')

    app.run(host=host, port=int(port), threaded=True)
