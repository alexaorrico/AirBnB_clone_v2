#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)


app.register_blueprint(app_views)

cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """closes session"""
    storage.close()


@app.errorhandler(404)
def error_message(error):
    """error message"""
    return make_response(jsonify({'error': 'Not found'}), 404)


API_HOST = getenv("HBNB_API_HOST", default="0.0.0.0")
API_PORT = getenv("HBNB_API_PORT", default=5000)


if __name__ == '__main__':

    app.run(host=API_HOST, port=API_PORT, threaded=True, debug=True)
