#!/usr/bin/python3
""" """

from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

# Defining a teardown method
def close_storage(error=None):
    """Function that closes the storage"""
    storage.close()

# Registering the teardown method
app.teardown_appcontext(close_storage)


if __main__ == "__main__":
    HBNB_API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    HBNB_API_PORT = getenv("HBNB_API_PORT", 5000)
    threaded=True
    app.run(HBNB_API_HOST, HBNB_API_PORT, threaded=threaded)