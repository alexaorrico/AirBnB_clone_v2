#!/usr/bin/python3
"""Flask app for AirBnB api"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(*args):
    """Refresh storage"""
    storage.close()


@app.errorhandler(404)
def pageNotFound(*args):
    """Handler for 404 Not found errors"""
    return ({'error': 'Not found'}), 404


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
