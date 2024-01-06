#!/usr/bin/python3
"""
Creates a new Flask app
"""

from flask import Flask
from flask_cors import CORS
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import jsonify

app = Flask(__name__)
# Enable CORS
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.url_map.strict_slashes=False


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Removes the current SQLAlchemy Session object after each request.
    """
    storage.close()
    
# Error handlers for expected app behavior:
@app.errorhandler(404)
def not_found(error):
    """
    Return errmsg `Not Found`.
    """
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == '__main__':
    HOST = '0.0.0.0' if getenv('HBNB_API_HOST') is None else getenv('HBNB_API_HOST')
    PORT = '5000' if getenv('HBNB_API_PORT') is None else getenv('HBNB_API_PORT')
    app.run(host=HOST, port=PORT, threaded=True)
