#!/usr/bin/python3
"""
Contains the flask web app
"""

from api.v1.views import app_views
from flask import Flask
from models import storage
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """Delete all application"""
    storage.close()


if __name__ == "__main__":
    hostt = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    portt = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else "5000"
    app.run(host=hostt, port=portt, threaded=True)
