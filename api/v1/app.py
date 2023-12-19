#!/usr/bin/python3
"""app.py"""

from flask import Flask
from os import environ
from models import storage
from api.v1.views import app_views

# Create a variable app, instance of Flask
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle @app.teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    """Close the storage on teardown."""
    storage.close()

# Inside if __name__ == "__main__":, run your Flask server (variable app) with:
if __name__ == "__main__":
    """ Main Function """
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)