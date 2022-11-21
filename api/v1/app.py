#!/usr/bin/python3
"""
Sets up first endpoint that returns stats of the API
"""


from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    Calls storage.close
    """
    storage.close()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = "5000"
    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    if getenv("HBNB_API_PORT"):
        port = getenv("HBNB_API_PORT")

    app.run(host=host, port=port, threaded=True)
