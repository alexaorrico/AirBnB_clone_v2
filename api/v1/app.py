#!/usr/bin/python3
"""
    Main file of API,
    he store the Flask app and run the api
"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.route('/', strict_slashes=False)
def index ():
    return str(app.url_map)

@app.errorhandler(404)
def page_not_found(error):
    """
        Return a JSON error message. 
        This is used to display an error when the request cannot be found.

        @param error - The error that was encountered. Can be None.
        @return The JSON error message with the error message in it
    """
    return jsonify({"error": "not found"})


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

# Run the app with the default port 5000 threaded true
if __name__ == '__main__':
    app.run(
        host= os.environ.get('HBNB_API_HOST', '0.0.0.0'),
        port= os.environ.get('HBNB_API_PORT', '5000'), 
        threaded=True
    )