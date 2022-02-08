#!/usr/bin/python3
"""
app entry point
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

host = getenv("HBNB_API_HOST") or "0.0.0.0"
port = getenv("HBNB_API_PORT") or 5000


@app.teardown_appcontext
def teardown_appcontext(self):
    """Register a function to be called when the request
        fails,method that is called when
        the application crashes.
    """
    storage.close()


@app.errorhandler(404)
def error_404(e):
    """ Function that shows a state 404"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
