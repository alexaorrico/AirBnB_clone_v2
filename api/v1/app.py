#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views

# Create a Flask instance
app = Flask(__name__)

# Register the blueprint app_views to your Flask instance app
app.register_blueprint(app_views)

# Declare a method to handle @teardown_appcontext that calls storage.close()
@app.teardown_appcontext
def close_storage(exception):
    storage.close()


if __name__ == "__main__":
    import os

    # Get the host from the environment variable HBNB_API_HOST or use '0.0.0.0' if not defined
    host = os.environ.get('HBNB_API_HOST', default='0.0.0.0')

    # Get the port from the environment variable HBNB_API_PORT or use 5000 if not defined
    port = int(os.environ.get('HBNB_API_PORT', default=500))

    # Run the Flask server (variable app) with threaded=True
    app.run(host=host, port=port, threaded=True)
