#!/usr/bin/python3

"""

This module creates and configures the Flask app, registers blueprints,
and sets up the teardown_appcontext to close the database connection.

"""

from flask import Flask
from models import storage
import os
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Teardown appcontext method to close the database connection."""
    storage.close()


if __name__ == "__main__":
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(os.getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
