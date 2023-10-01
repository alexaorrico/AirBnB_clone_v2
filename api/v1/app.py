#!/usr/bin/python3
"""first endpoint (route) will be to return the status of your API"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os
from flask import Flask, jsonify, make_response, render_template, url_for
from werkzeug.exceptions import HTTPException


app = Flask(__name__)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


# global strict slashes
app.url_map.strict_slashes = False


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    """Start flask app"""
    setup_global_errors()
    app.run(host=host, port=port, threaded=True)
