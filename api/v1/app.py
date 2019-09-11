#!/usr/bin/python3
"""Create conection to server"""

from models import storage
from flask import Flask, jsonify
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

host = str(os.environ.get("HBNB_API_HOST", "0.0.0.0"))
port = int(os.environ.get("HBNB_API_PORT", 5000))


@app.teardown_appcontext
def teardown(exception=None):
    """declare a method to handle @app.teardown_appcontext """
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """Handler 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(threaded=True, debug=True, host=host, port=port)
