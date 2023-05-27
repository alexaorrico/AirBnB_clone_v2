#!/usr/bin/python3
""" This module starts a flask application """
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()

if __name__ == "__main__":
    """Set the host and port based on environment variables or default values"""
    host = os.environ.get("HBNB_API_HOST", "0.0.0.0")
    port = int(os.environ.get("HBNB_API_PORT", 5000))

    """Run the Flask server"""
    app.run(host=host, port=port, threaded=True)
