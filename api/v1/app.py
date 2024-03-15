#!/usr/bin/python3
""" Starts instance of Flask application for communication with API """
from flask import Flask
import os
from models import storage
from api.v1.views import app_views


# Set up instance of Flask
app = Flask(__name__)


# Register app_view blueprint
app.register_blueprint(app_views)


# Teardown 
@app.teardown_appcontext
def teardown_db():
    storage.close()


if __name__ == "__main__":
    # Get environment variables and set defaults
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    
    # Run Flask app, with debug and threaded options
    app.run(host=host, port=port, debug=True, threaded=True)
