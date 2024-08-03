#!/usr/bin/python3

"""
This is our flask application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage


app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False
host = getenv("HBNB_API_HOST", "0.0.0.0")
port = getenv("HBNB_API_PORT", "5000")


@app.teardown_appcontext
def teardown(exception):
    """
    This is our teardown function.
    Calls close()
    """
    storage.close()


@app.errorhandler(404)
def handle_404(exception):
    """
    Handler for 404 error
    Returns 404 json
    """
    data = {
        "error": "Not found"
    }

    resp = jsonify(data)
    resp.status_code = 404

    return (resp)


if __name__ == "__main__":
    app.run(host, port, threaded=True, debug=True)
