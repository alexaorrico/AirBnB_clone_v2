#!/usr/bin/python3
"""Python api built with flask"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(exception):
    '''Calls storage close on appcontext'''
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    '''Returns a JSON formatted 404 status code'''
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(400)
def error_handler2(error):
    '''Returns a JSON formatted 404 status code'''
    return make_response(jsonify({'error': 'Not a JSON'}), 400)


if __name__ == "__main__":
    host = getenv('nope_API_HOST', '0.0.0.0')
    port = getenv('nope_API_PORT', 5000)
    app.run(host=host, port=int(port), threaded=True)
