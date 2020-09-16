#!/usr/bin/python3
""" the begining of everything """
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from os import getenv
from models import storage
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def tear_down(self):
    """closing storage"""
    storage.close()

if __name__ == '__main__':
    host_flask = getenv("HBNB_API_HOST") or '0.0.0.0'
    port_flask = getenv("HBNB_API_PORT") or '5000'
    app.run(host=host_flask, port=port_flask, threaded=True)
