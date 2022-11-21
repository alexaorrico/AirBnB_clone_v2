#!/usr/bin/python3
"""
    v1 app codebase
"""

from api.v1.views import app_views
from flask import Flask
from models import storage
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def exit():
    """Cleaning up after stops running"""
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    if not host:
        host = '0.0.0.0'
    port = os.getenv('HBNB_API_PORT')
    if not port:
        port = 5000
    app.run(host, port, threaded=True)
