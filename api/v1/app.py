#!/usr/bin/python3
"""
Creates Flask instance and contains handlers for 404 Not found Error and Method
for terminating storage session.
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown_routine(Exception):
    """
    Function to terminate db session after each request is over.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Handler method for any requests that don't match a resource."""
    return make_response(jsonify({'error': "Not found"}), 404)


if __name__ == "__main__":
    """Method that will run the Flask instance when called from terminal"""
    app.run(host=host, port=port, threaded=True)
