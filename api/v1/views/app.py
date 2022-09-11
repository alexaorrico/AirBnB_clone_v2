#!/usr/bin/python3
"""
the app module
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(exception):
    """"
    calls storage.close() method
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if host is None:
        host = "0.0.0.0"
    if port is None:
        port = "5000"
    app.run(host, port, threaded=True)
