#!/usr/bin/python3
"""
Main Flask application for the AirBnB clone API.
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def close_storage(exception):
    """
    Closes the storage on teardown.

    Args:
        exception: Unused argument.

    Returns:
        None
    """
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
