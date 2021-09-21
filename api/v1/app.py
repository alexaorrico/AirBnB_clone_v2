#!/usr/bin/python3
"""app module"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_storage(exception):
    """close storage connection"""
    storage.close()


@app.errorhandler(404)
def resource_not_found(e):
    """page not found"""
    msg = {"error": "Not found"}
    return make_response(jsonify(msg), 404)


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')
    app.run(host=host, port=port, threaded=True)
