#!/usr/bin/python3
"""
    Starts a flask application
"""

from api.v1.views import app_views
from flask_cors import CORS
from flask import Flask, jsonify
from models import storage
from os import getenv


host = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
port = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5000'


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.errorhandler(404)
def page_not_found(error):
    """
        Handles 404 errors
    """
    return jsonify({'error': 'Not found'}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """
        Called at the end of a request
    """
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
