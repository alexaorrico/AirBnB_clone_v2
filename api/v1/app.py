#!/usr/bin/python3
""" Flask Application """
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
    # host = environment variable HBNB_API_HOST or 0.0.0.0 if not defined
    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    # port = environment variable HBNB_API_PORT or 5000 if not defined
    port = environ.get('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)