#!/usr/bin/python3
"""API module entry point"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os
import json
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontent(exception):
    """Calls storage.close"""
    storage.close()


@app.errorhandler(404)
def page_not_found(exception):
    """404 Page Not Found Error Handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
