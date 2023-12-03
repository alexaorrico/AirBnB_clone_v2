#!/usr/bin/python3
"""
The following script creates a Flask app,
and registers the blueprint 'api_views' to the Flask instance app
"""


from os import getenv
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


# Enabling CORS and allowing for origins:
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})


app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown_engine(exception):
    """
    The following method removes the current SQLAlchemy
    Session object after each request
    """
    storage.close()


# Updated comment for error handler

@app.errorhandler(404)
def not_found(error):
    """
    The following method returns the error msg “Not Found”
    for custom 404 error handling
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    API_HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
    API_PORT = int(getenv('HBNB_API_PORT', default=5000))
    app.run(host=API_HOST, port=API_PORT, threaded=True)
