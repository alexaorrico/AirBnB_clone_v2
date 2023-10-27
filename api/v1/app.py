#!/usr/bin/python3
"""
API Application Module

Sets up and starts an API application.
Initializes the Flask application for the API and sets up the API routes and
configuration.
"""

import os
from flask import Flask
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage_session(self):
    """ Delete the current SQLAlchemy Session """
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))
    app.run(host=host, port=port, threaded=True)
