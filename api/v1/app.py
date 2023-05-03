#!/usr/bin/python3
"""This is our basic app file"""
from api.v1.views import app_views
from models import storage
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from os import getenv
app = Flask(__name__)
CORS = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def error404(error):
    """Returnas a 404 errro as a json response"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = getenv('HBNB_API_PORT')
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
