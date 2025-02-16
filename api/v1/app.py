#!/usr/bin/python3
"""Flask App for the AirBnB API"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

# Register the Blueprint
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Closes storage session"""
    storage.close()

if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

