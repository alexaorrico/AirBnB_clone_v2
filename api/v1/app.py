#!/usr/bin/python3
"""	This is app.py for v1 api """

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception=None):
    """Closes the Session"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """Returns A Custom 404 Not Found In Json Format"""
    error_message = {'error': 'Not Found'}
    response = jsonify(error_message)
    response.status_code = 404
    return response


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
    PORT = getenv('HBNB_API_PORT', default=5000)

    app.run(HOST, int(PORT), threaded=True)
