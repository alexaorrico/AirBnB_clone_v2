#!/usr/bin/python3
"""app.py module"""
from api.v1.views import app_views
from flask import Flask, Blueprint, make_response
from flask_cors import CORS
from models import storage
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

app_cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.teardown_appcontext
def teardown_db(exception):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response({"error": "Not found"}, 404)
    # return {"error": "Not found"}  # returns status code 200


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", "0.0.0.0"),  # 0.0.0.0 if no env set
        port=getenv("HBNB_API_PORT", 5000),
        threaded=True,
    )
