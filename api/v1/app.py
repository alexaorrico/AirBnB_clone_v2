#!/usr/bin/python3
"""starts a Flask web application"""
from os import getenv

from flask import Flask
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exec):
    """Calls storage close method"""
    storage.close()


@app.errorhandler(404)
def not_found(e):
    """Returns 404 error in JSON"""
    e = {"error": "Not found"}
    return e, 404


@app.errorhandler(400)
def error_400(e):
    """Returns 400 error in JSON"""
    if not e:
        return {"error": "400"}
    else:
        return e, 400


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host, port, threaded=True)
