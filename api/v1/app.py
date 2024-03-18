#!/usr/bin/python3
"""Module containing API engine"""
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
import os
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

if 'HBNB_API_HOST' in os.environ:
    host = os.getenv('HBNB_API_HOST')
else:
    host = '0.0.0.0'
if 'HBNB_API_PORT' in os.environ:
    port = os.getenv('HBNB_API_PORT')
else:
    port = '5000'


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """ 404 but in JSON :( """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
