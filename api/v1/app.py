#!/usr/bin/python3
"""Creates a Flask web app"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(Exception):
    """closes storage"""
    storage.close()


@app.errorhandler(404)
def error_status(error):
    """handles 404 errors"""
    return jsonify(error="Not found"), 404


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=getenv("HBNB_API_PORT", 5000),
            threaded=True)
