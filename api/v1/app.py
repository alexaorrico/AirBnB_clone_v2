#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import Flask, make_response, jsonify


app = Flask(__name__)

app.register_blueprint(app_views)

@app.teardown_appcontext
def close(self):
    if storage is not None:
        storage.close()

@app.errorhandler(404)
def error_404(err):
    """get the error 404  when the request is not available in json"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host, port, threaded=True)
