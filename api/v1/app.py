#!/usr/bin/python3
# app.py

# Import necessary modules
from flask import Flask
import os
from models import storage
from api.v1.views import app_views

# Create a Flask app instance
app = Flask(__name__)

# Register the blueprint for API views with a URL prefix
app.register_blueprint(app_views, url_prefix="/api/v1")

# Teardown app context to close the storage connection
@app.teardown_appcontext
def teardown_appcontext(exception):
    """Teardown app context"""
    storage.close()

# Run the Flask app if this script is executed
if __name__ == "__main__":
    # Get host and port from environment variables or use default values
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    # Run the Flask app with the specified host, port, and threaded option
    app.run(host=host, port=port, threaded=True)
