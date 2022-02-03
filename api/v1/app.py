#!/usr/bin/python3
'''Contains a Flask web application API.
'''
import os
from flask import Flask, jsonify

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
'''The Flask web application instance.'''
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_flask(exception):
    '''The Flask app/request context end event listener.'''
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''Handles the 404 HTTP error code.'''
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    app_host = os.getenv('HBNB_API_HOST')
    app_port = os.getenv('HBNB_API_PORT')
    app.run(
        host=app_host if app_host else '0.0.0.0',
        port=app_port if app_port else '5000',
        threaded=True
    )
