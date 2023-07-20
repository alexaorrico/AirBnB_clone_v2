#!/usr/bin/python3
"""Api/v1/app.py"""
from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

def register_blueprints(app):
    """Register the blueprint app_views to the Flask instance app."""
    app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """Closes the storage engine when the application context is torn down."""
    storage.close()

if __name__ == "__main__":
    """Set default values for host and port if not defined in the environment."""
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
