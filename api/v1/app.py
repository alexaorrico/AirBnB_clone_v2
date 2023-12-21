#!/usr/bin/python3
"""module for app file of hbnb clone"""

from api.v1.views import app_views
from flask import Flask
from models import storage
import os


# set up app_views blueprint and flask instance
app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """close storage"""
    storage.close()


if __name__ == "__main__":
    HBNB_API_HOST = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    HBNB_API_PORT = os.getenv("HBNB_API_PORT", default='5000')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
