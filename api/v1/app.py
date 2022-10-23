#!/usr/bin/python3
"""return status of route"""
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
CORS(app, resources=r"/*", origins="0.0.0.0")
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """ Gives the 404 not found page """
    return (jsonify({"error":"Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if (not host):
        host = "0.0.0.0"
    if (not port):
        port = 5000
    app.run(host=host, port=port, threaded=True)