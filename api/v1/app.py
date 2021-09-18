#!/usr/bin/python3
""" Star the api with Flask"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def close_storage(self):
    """[close de db call close]
    """
    storage.close()
  
@app.handler_error(404)
def error_status(error):
    """[return the error 404 in json format]

    Args:
        error: [status of the server]
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api_host = getenv('HBNB_API_HOST', default='0.0.0.0')
    api_port = getenv('HBNB_API_PORT', default=5000)
    app.run(host=api_host, port=int(api_port), threaded=True)
