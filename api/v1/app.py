#!/usr/bin/python3
"""craetin flask app"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """close the storage"""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=port, threaded=True)
