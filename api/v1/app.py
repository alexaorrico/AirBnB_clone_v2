#!/usr/bin/python3
"""
This is the app module
"""

from flask import Flask
from os import getenv
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def session_close(exception):
    """
    This function close session
    """
    storage.close()

if __name__ == "__main__":
    app.run(
        host = getenv('HBNB_API_HOST') or '0.0.0.0',
        port = getenv('HBNB_API_PORT') or '5000',
        threaded = True
    )
