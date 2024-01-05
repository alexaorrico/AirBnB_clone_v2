#!/usr/bin/python3
"""
Flask API Application

This script defines a Flask application for an API.
It includes a Blueprint named 'app_views' for handling API routes.
The application is configured to handle the endpoint '/status'
\tprovided in the 'app_views' Blueprint.

"""
from flask import Flask
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_flask(exception):
    """
    Teardown method to close the database connection when the Flask application
    context ends.

    Parameters:
    - exception: An exception object if an exception occurred during processing
    """
    storage.close()


if __name__ == "__main__":
    app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    app_port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(
        host=app_host,
        port=app_port,
        threaded=True
    )
