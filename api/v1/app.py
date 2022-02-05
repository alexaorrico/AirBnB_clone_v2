#!/usr/bin/python3
"""
    api app flask
"""
from flask import Flask, jsonify
from os import getenv
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def ERROR_404(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown(self):
    """method to handle teardown"""
    storage.close()


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST') or "0.0.0.0"
    port = getenv('HBNB_API_PORT') or 5000

    app.run(host=host, port=int(port), threaded=True)
