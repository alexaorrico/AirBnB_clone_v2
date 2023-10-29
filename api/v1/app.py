#!/usr/bin/python3
"""Module contains flask app"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS
from flask import make_response

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def closeStorage(self):
    """Closes the storage session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(err):
    """Custom 404 page not found json error message"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    useHost = getenv('HBNB_API_HOST') or '0.0.0.0'
    usePort = getenv('HBNB_API_PORT') or 5000

    app.run(host=useHost, port=usePort, threaded=True)
