#!/usr/bin/python3
""" This module starts a flask application """
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def remove(exception):
    """ removes the current session """

    storage.close()


@app.errorhandler(404)
def not_found(e):
    """ configures 404 error response """

    return jsonify({"error": "Not found"}), e.code


if __name__ == "__main__":
    env_host = os.getenv("HBNB_API_HOST")
    env_port = os.getenv("HBNB_API_PORT")

    app.run(host=env_host if env_host else "0.0.0.0",
            port=env_port if env_port else 5000,
            threaded=True)
