#!/usr/bin/python3
"""
API instance
"""
from unicodedata import category
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def storage_close(self):
    """
    Calls storage.close()
    """
    storage.close()


@app.errorhandler(404)
def notfound_404(error):
    """
    Retrieves the number of each objects by type.
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
