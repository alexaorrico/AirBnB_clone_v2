#!/usr/bin/python3
"""
module for api configuration
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resource={r"/api/v1/*":{"origin":"0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """ tear doen appcontext """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """handling error when non-existing url is querired"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", 5000)
    app.run(host, port, threaded=True)
