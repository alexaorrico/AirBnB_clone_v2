#!/usr/bin/python3
"""Flask RESTful application"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
# app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    """Close the storage"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") or "0.0.0.0"
    port = getenv("HBNB_API_PORT") or 5000
    app.run(host=host, port=int(port), threaded=True)
