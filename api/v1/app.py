#!/usr/bin/python3
"""An app for registering a blueprint and starting a server"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown(self):
    """Close query"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return JSON 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", "5000"))
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host, port, threaded=True)
