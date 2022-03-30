#!/usr/bin/python3

"""
Module to check the status of the API
"""

from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=["http://0.0.0.0:5000", "/*"])

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    '''This method closes the storage object'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    not_found_error = {'error': 'Not found'}
    return make_response(jsonify(not_found_error), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', threaded=True)
