#!/usr/bin/python3

""" Flask application for aibrnb clone"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
import os
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage(exception=None):
    """closes current sqlalchemy session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """ Provides a JSON-formatted response with a 404 status code. """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    """Main function for flask app"""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True, debug=True)