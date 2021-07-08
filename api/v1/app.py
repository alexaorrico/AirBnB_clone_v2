#!/usr/bin/python3
"""
module to create Flask app that works with the API
"""
from models import storage
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config.update(JSONIFY_PRETTYPRINT_REGULAR=True)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(self):
    """
    tears down
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    error handler for 404
    """
    return (jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
