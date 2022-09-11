#!/usr/bin/python3
"""first endpoint (route) will be to return the status of API"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv
from flask import jsonify
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """close sessions"""
    storage.close()


@app.errorhandler(404)
def handle_bad_request(e):
    """hanlder error 404"""
    error = {}
    error['error'] = "Not found"
    return jsonify(error), 404


if getenv("HBNB_API_HOST") is not None:
    api_host = getenv("HBNB_API_HOST")
else:
    api_host = "0.0.0.0"

if getenv("HBNB_API_PORT") is not None:
    api_port = getenv("HBNB_API_PORT")
else:
    api_port = "0.0.0.0"

if __name__ == '__main__':
    app.run(
            host=api_host,
            port=api_port,
            threaded=True)
