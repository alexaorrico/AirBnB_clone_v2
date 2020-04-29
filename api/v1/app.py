#!/usr/bin/python3
"""
Create API.
"""


from flask import Flask, jsonify
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close(exc):
    """
    Terminate session.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return not found modified JSON."""
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")
    app.run(host=host, port=port, threaded=True)
