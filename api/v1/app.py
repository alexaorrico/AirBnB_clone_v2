#!/usr/bin/python3
"""Flask RESTful application"""
from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def teardown(self):
    """Close the storage"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=int(getenv("HBNB_API_PORT", default=5000)),
        threaded=True
    )
