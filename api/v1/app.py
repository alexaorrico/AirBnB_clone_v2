#!/usr/bin/python3
"""Main Flask app"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, origins="0.0.0.0")
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """Teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Handle error 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=os.getenv('HBNB_API_HOST'),
        port=os.getenv('HBNB_API_PORT'),
        threaded=True)
