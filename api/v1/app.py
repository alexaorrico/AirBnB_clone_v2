#!/usr/bin/python3
""" initializes Flask application """
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exception):
    """ closes db """
    return storage.close()


@app.errorhandler(404)
def not_found(error):
    response = jsonify({'error': 'Not Found'})
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', threaded=True, debug=True)
