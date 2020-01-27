#!/usr/bin/python3
""" first endpoint"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
try:
    app.register_blueprint(app_views, url_prefix="/api/v1")

    @app.teardown_appcontext
    def teardown_storage(e):
        """close"""
        storage.close()
except:
    print("error")

if __name__ == "__main__":
    app.run(host=os.environ.get("HBNB_API_HOST", "0.0.0.0"),
            port=os.environ.get("HBNB_API_PORT", "5000"), threaded=True)
