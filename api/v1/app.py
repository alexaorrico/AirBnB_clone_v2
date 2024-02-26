#!/usr/bin/python3
"""AirBnB API"""
from os import getenv
from flask import Flask
from flask import jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_teardown(exception):
    """Closes the storage session"""
    storage.close()


if __name__ == "__main__":
    app.run(
        host=getenv("HBNB_API_HOST", default="0.0.0.0"),
        port=getenv("HBNB_API_PORT", default=5000),
        threaded=True
    )
