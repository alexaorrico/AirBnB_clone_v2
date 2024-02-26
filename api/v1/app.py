#!/usr/bin/python3
"""AirBnB API"""
from os import getenv
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(exception):
    """Closes the storage session"""
    storage.close()


@app.errorhandler(404)
def notfound(error):
    """Handles 404 Not found errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default=5000),
        threaded=True
    )
