#!/usr/bin/python3
"""
Starts up a flask web app
"""
from models import storage
from flask import Flask, make_response, jsonify
from api.v1.views import app_views
from os import getenv, environ

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def teardown_appcontext(response_or_exc):
    storage.close()


if __name__ == "__main__":
    host = '0.0.0.0'
    port = 5000
    if environ.get('HBNB_API_HOST'):
        host = getenv('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT'):
        port = getenv('HBNB_API_PORT')
    app.run(host=host, port=int(port), threaded=True)
