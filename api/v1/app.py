#!/usr/bin/python3
"""Register blueprint"""
from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    """Remove the current SQLAlchemy Session
           Parameters:
               error [str]: an error message or exception
    """
    storage.close()


@app.errorhandler(404)
def not_found(message):
    """Handles the 404 status code
           Parameters:
               message [str]: a custom message to display
           Returns:
               The HTTP response for the request
    """
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', default=5000)),
        threaded=True
    )
