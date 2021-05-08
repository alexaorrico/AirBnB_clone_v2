#!/usr/bin/python3
"""
Flask web application
"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
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


if __name__ == "__main__":
    """ """
    app.run(host=host, port=port)
