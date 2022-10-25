#!/usr/bin/python3
"""
summary_
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
"""
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
"""
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """runs this method when app context tears down"""
    storage.close()


@app.errorhandler(404)
def not_found(err):
    """handle 404 error and return JSON-formatted 404 status code response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
