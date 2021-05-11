#!/usr/bin/python3
"""API entry point"""

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify
from flask import make_response
import os
import json
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(stiven):
    """teardown function"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Error handler for not found route"""
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, debug=True, threaded=True)
