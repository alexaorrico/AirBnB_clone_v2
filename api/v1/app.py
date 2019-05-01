#!/usr/bin/python3
"""Entry point for Airbnb_clone_v3 api calls."""
from os import getenv
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Returns a JSON-formatted 404 status code response."""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_storage(exc):
    """Closes the storage session after every request."""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default="5000"),
        threaded=True
    )
