#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template.
This module sets up a Flask application with CORS configuration.
"""

# Importing necessary modules and packages
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS  # Import CORS module
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# Global CORS Configuration: Allow /* for 0.0.0.0
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

# Teardown context function
@app.teardown_appcontext
def teardown_db(exception):
    """
    After each request, this method calls .close() on the current SQLAlchemy Session.
    """
    storage.close()

# Global error handler function
@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Global Route to handle All Error Status Codes.
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

# Setup global errors
def setup_global_errors():
    """
    Update HTTPException Class with custom error function.
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)

if __name__ == "__main__":
    """
    MAIN Flask App.
    """
    # Initializes global error handling
    setup_global_errors()
    # Start Flask app
    app.run(host=host, port=port)
