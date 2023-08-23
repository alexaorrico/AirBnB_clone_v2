#!/usr/bin/python3
"""
Imports
"""
from flask import Flask
from os import environ
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


def close(err):
    storage.close()


if __name__ == "__main__":
    app.run(host=environ.get("HBNB_API_HOST", "0.0.0.0"),
            port=environ.get("HBNB_API_PORT", "5000"), threaded=True)


@app.errorhandler(404)
def not_found(error):
    return {
        "error": "Not found"
    }, 404
