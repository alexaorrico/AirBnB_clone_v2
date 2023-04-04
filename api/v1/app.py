#!/usr/bin/python3
"""
App module that creates a Flask instance and registers blueprints to it.
"""
from flask import Flask, make_response
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 scenario (page not found)
    """
    code = exception.__str__().split()[0]
    message = {"error": "Not found"}
    return make_response(message, code)


@app.teardown_appcontext
def close_storage(exception):
    """
    Closes the storage instance when the app context is torn down.
    """
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = os.environ.get("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
