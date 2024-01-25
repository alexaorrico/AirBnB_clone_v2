#!/usr/bin/python3
"""introducing a flask file"""
from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
import os


app = Flask(__name__)
CORS(app, resources={r'/api/v1/*': {'origins': '0.0.0.0'}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def error_handler(error):
    """Handles error 404"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True, debug=True)
