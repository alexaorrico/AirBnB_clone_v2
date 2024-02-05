#!/usr/bin/python3
"""AirBnB Clone API configuration file"""

from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)


# Register the blueprint
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_app(exception):
    """disconnect the db session """
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
