#!/usr/bin/python3
""" This module creates a Flask instance "app" and registers the blueprint app_views """

import os
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)

# Register the blueprint app_views to the Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def teardown_db(exception):
    storage.close()

if __name__ == "__main__":
    # Get the host and port from environment variables or use default values
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", "5000"))

    # Run the Flask server with the specified host, port, and threaded=True
    # to set as environmental variables open editor to ~/.bashrc and add
    # export HBNB_API_HOST=0.0.0.0 and export HBNB_API_PORT=5000
    # then run <source ~/.bashrc> to update the environmental variables
    app.run(host=host, port=port, threaded=True)
