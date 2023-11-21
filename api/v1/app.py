#!/usr/bin/python3
""" Creates the api """

from flask import Flask, Blueprint, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)


@app.teardown_appcontext
def closedb(exception):
    """calls the storage.close()"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """returns a 404 error"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=port, threaded=True)
