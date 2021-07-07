#!/usr/bin/python3
""" app file
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)

h = os.environ.get("HBNB_API_HOST", "0.0.0.0")
p = os.environ.get("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def close(exception=None):
    """
    teardown function
    """
    storage.close()


@app.errorhandler(404)
def _handle_api_error(ex):
    """
    errorhandler funtion
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=str(h), port=int(p), threaded=True)
