#!/usr/bin/python3
""" api """

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def closer(close):
    """ closes """
    storage.close()


@app.errorhandler(404)
def fourOfour(e):
    return (jsonify(error="Not found"), 404)


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST"):
        host = os.getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if os.getenv("HBNB_API_PORT"):
        port = int(os.getenv("HBNB_API_PORT"))
    else:
        port = 5000
    app.env = 'development'
    app.run(host=host, port=port, threaded=True)
