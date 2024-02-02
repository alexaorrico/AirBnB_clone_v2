#!/usr/bin/python3
""" The implemtation of tha application"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_app(exc=None):
    storage.close()


if __name__ == "__main__":
    HOST = os.getenv("HBNB_API_HOST", "0.0.0.0")
    PORT = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=HOST, port=PORT, threaded=True)
