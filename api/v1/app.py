#!/usr/bin/python3
"""the main entrance to the api"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def teardown_db(execption):
    """Closes the database session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handles 404 error"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(400)
def bad_request(error):
    """Handles 400 error"""
    return jsonify({"error": error.description}), 400


if __name__ == "__main__":
    app.run(
        host=getenv('HBNB_API_HOST', '0.0.0.0'),
        port=int(getenv('HBNB_API_PORT', '5000')),
        threaded=True
    )
