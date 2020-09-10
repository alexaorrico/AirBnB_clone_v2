#!/usr/bin/python3
"""comment"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_app(self):
    """comment"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """deffo pleeffofo"""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    if environ.get('HBNB_API_HOST') is None:
        hos = "0.0.0.0"
    else:
        hos = environ.get('HBNB_API_HOST')
    if environ.get('HBNB_API_PORT') is None:
        por = 5000
    else:
        por = environ.get('HBNB_API_PORT')
    app.run(host=hos, port=por, threaded=True)
