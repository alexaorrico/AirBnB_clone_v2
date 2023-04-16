#!/usr/bin/python3
"""Start of Flask app"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


@app.teardown_appcontext
def close_storage(exception):
    storage.close()


@app.errorhandler(404)
def handle_404(e):
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    """Starting flask server"""
    host = '0.0.0.0'
    port = '5000'
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")
    app.run(host=host, port=port, threaded=True)
