#!/usr/bin/python3
""" Module for app.py """

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

# Create Flask app
app = Flask(__name__)

# Create blueprint
app.register_blueprint(app_views)


# Declare method to handle @app.teardown that calls storage.close
@app.teardown_appcontext
def teardown(error):
    """ Method to close storage """
    storage.close()


if __name__ == "__main__":
    """Main method"""""
    host = getenv("HBNB_API_HOST")
    port = getenv("HBNB_API_PORT")
    if not host:
        host = "0.0.0.0"
    if not port:
        port = "5000"
    app.run(host=host, port=port, threaded=True)
