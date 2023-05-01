#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDown():
    """
    teardown function

    """
    storage.close()


@app.errorhandler(404)
def handle_404():
    """
    handles 404 error

    """
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST"), getenv("HBNB_API_PORT")), threaded=True, debug=True)
