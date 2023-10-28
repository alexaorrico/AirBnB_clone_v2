#!/usr/bin/python3
""" Flask WEB Server """
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
CORS(app, origins="0.0.0.0")
hostapi = getenv('HBNB_API_HOST', '0.0.0.0')
portapi = getenv('HBNB_API_PORT', '5000')


@app.teardown_appcontext
def commit_data(error):
    """ Close Database """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Not Found -> (404) """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    app.run(host=hostapi, port=portapi, threaded=True)
