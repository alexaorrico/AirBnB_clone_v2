#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """teardown storage session"""
    storage.close()


@app.errorhandler(404)
def error_404(self):
    """ Handler for 404 error. """
    return jsonify(
        {
            "error": "Not found"
        })


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True)
