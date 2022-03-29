#!/usr/bin/python3

"""setting up api functions"""
from api.v1.views import app_views
from flask import Flask, jsonify
# from flask_cors import CORS
from models import storage
import os


app = Flask(__name__)
# CORS(app)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """calls storage.close on teardown"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """handles 404 errors by returning JSON formatted status code"""
    return jsonify({"error": "Not found"}), 404


if "HBNB_API_HOST" in os.environ:
    host = os.getenv("HBNB_API_HOST")
else:
    host = "0.0.0.0"

if "HBNB_API_PORT" in os.environ:
    port = os.getenv("HBNB_API_PORT")
else:
    port = 5000

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
