#!/usr/bin/python3
"""Flask Application for API"""

from flask import Flask
from flask_cors import CORS  # Import CORS
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Enable CORS for all origins (you can modify this later for production)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})  # Allow all origins for development

# Register Blueprint
app.register_blueprint(app_views)

# Close storage when request ends
@app.teardown_appcontext
def close_storage(exception):
    """Calls storage.close()"""
    storage.close()

if __name__ == "__main__":
    # Get environment variables or use defaults
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))

    # Run Flask app
    app.run(host=host, port=port, threaded=True)

