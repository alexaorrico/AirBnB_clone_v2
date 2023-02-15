#!/usr/bin/python3
""" flask integration of Airbnb clone static HTML templates """
from flask import Flask
from models import storage
#.models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app():
    """closes the app and all connections"""
    storage.close()


if __name__ == "__manin__":
    host = getenv(HBNB_API_HOST, "0.0.0.0")
    port = getenv(HBNB_API_PORT, "5000")
    app.run(host=host, port=port, threaded=True)
