#!/usr/bin/python3
"""AirBnb flask APP"""
from flask import Flask
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def closeStorage(error):
    """Method to close storage"""
    storage.close()


if __name__ == "__main__":
    app.debug = True
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
