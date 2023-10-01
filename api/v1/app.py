#!/usr/bin/python3
"""
This module defines a Flask application instance.

The Flask application instance is named app. It is configured to register
the blueprint app_views and close the storage engine after each request.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    Close the storage engine.

    This function is called after each request. It closes the storage engine
    to ensure that the SQLAlchemy session is properly removed.
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
