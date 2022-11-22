#!/usr/bin/python3
"""
    Flask file which starts application
"""
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """ method which calls close method on storage"""
    storage.close()


@app.errorhandler(404)
def handle_error(error):
    return make_response(jsonify({'error': 'Not found'}))


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True, debug=True)
