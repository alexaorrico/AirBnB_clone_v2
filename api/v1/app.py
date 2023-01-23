#!/usr/bin/python3
"""
Flask App integrated with AirBnB static
"""
from flask import Flask, Blueprint, abort, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger
from models import storage

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

# begin flask page rendering


@app.teardown_appcontext
def teardown(exception):
    """Close the current storage session"""
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """
      Global Route to handle all errors status code
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'Not found':
            err.description = 'Not found'
        msg = {'error': err.description}
        code = err.code
    else:
        msg = {'error': err}
        code = 500
    return make_response(jsonify(msg), code)


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    # start Flask app
    app.run(host=host, port=port, threaded=True)
