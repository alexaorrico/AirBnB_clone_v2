#!/usr/bin/python3

"""Api Interface"""
from os import getenv
from flask import Flask
from flask.helpers import make_response
from flask.json import jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDown(exc):
    """Close the session and request a new one once the application context is
    poped"""
    storage.close()


@app.errorhandler(404)
def on_error_404(e):
    """Defines error handler  for 404"""
    return make_response(jsonify(error="Not found"), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    if port and host:
        app.run(host=host, port=int(port), threaded=True)
