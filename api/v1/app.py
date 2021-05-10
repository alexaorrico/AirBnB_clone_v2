#!/usr/bin/python3
""" Flask """
from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="0.0.0.0")
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown(exception):
    """Close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    return JSON 404
    """
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    my_host = os.getenv('HBNB_API_HOST')
    my_port = os.getenv('HBNB_API_PORT')
    app.run(host=my_host, port=my_port, threaded=True)
