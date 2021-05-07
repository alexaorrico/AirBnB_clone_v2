#!/usr/bin/python3
""" TBD """

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
HBNB_API_HOST = os.getenv("HBNB_API_HOST")
HBNB_API_PORT = os.getenv("HBNB_API_PORT")


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    if not HBNB_API_HOST:
        HBNB_API_HOST = "0.0.0.0"
    if not HBNB_API_PORT:
        HBNB_API_PORT = "5000"
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
