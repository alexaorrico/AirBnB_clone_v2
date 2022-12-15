#!/usr/bin/python3
"""immported modules pa"""
import os
from api.v1.views import app_views
from models import storage
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_this(self):
    """close the storage instance"""
    storage.close()


if __name__ == "__main__":
    """documented pa"""

    host = os.getenv('HBNB_API_HOST', default="0.0.0.0")
    port = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=host, port=port, threaded=True)