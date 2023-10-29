#!/usr/bin/python3
"""
This module defines the structure of the flask api
implementation for the project
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Teardown function to close connection
    when a query is complete
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host_env = getenv("HBNB_API_HOST")
    port_env = getenv("HBNB_API_PORT")
    host = host_env if host_env else "0.0.0.0"
    port = int(port_env) if port_env else 5000
    app.run(host=host, port=port)
