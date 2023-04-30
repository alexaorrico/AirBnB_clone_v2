#!/usr/bin/python3
"""
A Script that return the status of API
"""
from app.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS
from models import storage
import os
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
cors = CORS(app, resouces={r"/api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def teardown(exception):
    """
    Function that closes the current session
    on the SQLAlchemy
    """
    storage.close()


@app.errorhandler(404)
def error_handler(exception):
    """
    A route that handles 404 (not found) error
    on the event the global error fails.
    """
    return jsonify({"error": "Not found"})


@app.errorhandler(400)
def handle_400():
    """
    Handles 400 error
    """
    code = exception.__str__().split()[0]
    description = exception.description
    return make_response(jsonify({"error": description}), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global route to handle all errors
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
    HTTPException with custom error
    """
    for cls in HTTPException.__subclass__():
        app.register_error_handler(cls, global_error_handler)


if __name__ == '__main__':
    """Main Flask App entry point"""
    setup_global_errors()
    app.run(host=host, port=port debug=True)
