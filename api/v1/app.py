#!/usr/bin/python3
"""
Flask web application
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')

cors = CORS(app, resources={'/*': {'origins': host}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_down(Exception):
    """ """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """ """
    app.run(host=host, port=port)
