#!/usr/bin/python3
""" this area is for file decription """
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import environ
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_database(error):
    """ close db when the app is torn down"""
    storage.close()


@app.errorhandler(404)
def er_handler(error):
    """ handle error response 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    """ description for this methode"""
    port = environ.get('HBNB_API_PORT')
    host = environ.get('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
