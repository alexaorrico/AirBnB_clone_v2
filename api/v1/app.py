#!/usr/bin/python3

"""Run the main flask app"""

from api.v1.views import app_views
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_up(exception=None):
    """Method that calls storage close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """error 404 handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
