#!/usr/bin/python3
"""
flask application
"""

from flask import Flask
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Teardown method to close storage"""
    storage.close()


if __name__ == "__main__":
    # Get the host from the environment variable or use "0.0.0.0" as default
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    # Get the port from the environment variable or use 5000 as default
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
