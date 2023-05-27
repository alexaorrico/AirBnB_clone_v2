#!/usr/bin/python3
"""Starts a flask web app"""

from os import getenv
from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exec):
    storage.close()


if __name__ == "__main__":
    if (getenv("HBNB_API_HOST") and getenv("HBNB_API_PORT")):
        app.run(host=getenv("HBNB_API_HOST"), 
                port=getenv("HBNB_API_PORT"), threaded=True)
    else:
        app.run(host="0.0.0.0", port=5000, threaded=True)
