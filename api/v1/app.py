#!/usr/bin/python3
"""This module contain a web application"""

from flask import Flask, jsonify
app = Flask(__name__)
from models import storage
from api.v1.views import app_views
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exception):
    """close the session after every request"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """ the function is called when a page is not found """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5000
    app.run(host=host, port=port, threaded=True)
