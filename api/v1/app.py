#!/usr/bin/python3
"""Creating the API and returning the status"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from os import environ


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app:
    """Tears down by calling storage.close"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST",
                        default="0.0.0.0"),
            port=getenv("HBNB_API_PORT",
                        default="5000"),
            threaded=True)
