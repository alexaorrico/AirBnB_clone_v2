#!/usr/bin/python3
"""
    Creates a web app using Flask
"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views, url_prefix="/api/v1")
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.teardown_appcontext
def app_teardown(exception):
    """calls close on storage"""
    storage.close()


if __name__ == "__main__":
    apiHost, apiPort = getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT")
    if not apiHost:
        apiHost = '0.0.0.0'
    if not apiPort:
        apiPort = '5000'
    app.run(host=apiHost, port=apiPort, threaded=True)
