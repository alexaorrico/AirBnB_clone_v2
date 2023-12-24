#!/usr/bin/python3
"""
    Script that sets up a Flask application
"""
from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")


@app.teardown_appcontext
def teardown_appcontext(exeption):
    """ Function to close the storage connection """
    storage.close()


if __name__ == "__main__":
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
