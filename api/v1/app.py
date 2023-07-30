#!/usr/bin/python3
"""
Script that imports a Blueprint(app_views) and runs Flask
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_sess(exception):
    """close session"""
    return storage.close()


if __name__ == "__main__":

    h = getenv("HBNB_API_HOST")
    host = "0.0.0.0" if not h else h
    port = 5000 if not getenv("HBNB_API_PORT") else getenv("HBNB_API_PORT")

    app.run(host=host, port=port, threaded=True)
