#!/usr/bin/python3
"""AirBnb flask APP"""
from flask import Flask, jsonify
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closeStorage(error):
    """Method to close storage"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ Defines a custom error handler for 404 errors"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.debug = True
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
