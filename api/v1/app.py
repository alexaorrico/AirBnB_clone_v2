#!/usr/bin/python3
""" Creating an instance of Flask """
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv as env


app = Flask(__name__)
CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.errorhandler(404)
def handle_404(exception):
    """handles 404 scenario (page not found)"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def teardown(exception):
    """method closes storage session"""
    storage.close()


if __name__ == "__main__":
    app.run(host=env('HBNB_API_HOST'),
            port=env('HBNB_API_PORT'),
            threaded=True)
