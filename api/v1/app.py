#!/usr/bin/python3
"""
    flask application
"""
from flask import Blueprint, Flask, jsonify, make_response
from models import storage
from os import getenv
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closeDB(obj):
    """Close the database"""
    storage.close()


@app.errorhandler(404)
def handle_404(error):
    """handle 404 error page"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default='0.0.0.0')
    port = getenv("HBNB_API_PORT", default=5000)
    app.run(host, int(port), threaded=True)
