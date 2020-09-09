#!/usr/bin/python3
"""
app file for the api
"""
from os import getenv
from models import storage
from flask import Blueprint
from flask import Flask, jsonify
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """ method to handle @app.teardown_appcontext """
    storage.close()


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = getenv('HBNB_API_PORT', '5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
