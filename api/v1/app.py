#!/usr/bin/python3
"""
    app
"""
from flask import Flask
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(bruh):
    """ teardown """
    storage.close()


@app.errorhandler(404)
def heck(e):
    """ 404 """
    return (e or {"error": "Not found"}, 404)


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST") or "0.0.0.0",
        port=int(getenv("HBNB_API_PORT")) or 5000,
        threaded=True
    )
