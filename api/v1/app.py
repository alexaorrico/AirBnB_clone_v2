#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, make_response, jsonify, Blueprint
from models import storage
from api.v1.views import app_views
from werkzeug.exceptions import HTTPException
from os import getenv
from flask_cors import CORS


# Global Flask Application Variable: app
app = Flask(__name__)
app.url_map.strict_slashes = False
# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)
""" Cors access to selected resources from a different origin."""
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown_db(Exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


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
    Updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == "__main__":
    """
    Main Flask app
    """
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port, threaded=True)
