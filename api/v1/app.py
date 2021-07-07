#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv, environ


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app.env = 'development'
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)


@app.errorhandler(404)
def not_found(error):
    """Gives error message when any invalid
    url are requested
    """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcont(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == "__main__":
    hbnb_host = '0.0.0.0'
    hbnb_port = 5000
    if environ.get('HBNB_API_HOST'):
        hbnb_host = getenv('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT'):
        hbnb_port = getenv('HBNB_API_PORT')
    app.run(host=hbnb_host, port=int(hbnb_port), threaded=True, debug=False)
