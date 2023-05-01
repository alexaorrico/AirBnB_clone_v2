#!/usr/bin/python3

"""Flask app"""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def clean_up(exception=None):
    """ closes current session"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """returns JSON formatted 404 status"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),

            port=getenv('HBNB_API_PORT', default=5000),
            threaded=True, debug=True
            )
