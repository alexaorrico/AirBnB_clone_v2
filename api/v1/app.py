#!/usr/bin/python3

"""Bootstap for api"""

from api.v1.views import app_views
from models import storage
from os import getenv
from flask import Flask

app = Flask(__name__)

app.register_blueprint(app_views,url_prefix="/api/v1")


@app.teardown_appcontext
def teardown(exception):
    storage.close()


if __name__ == "__main__":
    app.run(getenv("HBNB_API_HOST", "0.0.0.0"), getenv(
        "HBNB_API_PORT", 5000),debug=True,threaded=True)
