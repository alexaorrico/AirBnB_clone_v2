#!/usr/bin/python3
""" start of a flask application"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv

app = Flask(__name__)


@app.teardown_appcontext
def close_session(self):
    """closes the application"""
    storage.close()

@app.errorhandler
def error404(self):
    """Error 404 for page"""
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    default_host = getenv('0.0.0.0')
    default_port =  getenv('5000')

    app.run(host=default_host, port=default_port, threaded=True)
