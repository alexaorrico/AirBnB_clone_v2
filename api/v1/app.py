#!/usr/bin/python3
"""A Flask app that used to make communication bettween #nt apps"""

# Importing modules from system files
import os
from flask import Flask

# Importing modules from my files
from api.v1.views import app_views
from models import storage


app = Flask(__name__)
"""Instances of Flask web application"""
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))


@app.teardown_appcontext
def teardown_flask(exception):
    """Closing The Storage after use."""
    storage.close()


if __name__ == "__main__":
    """To run api app, If debug is on means our output have a good view."""
    app.run(host=app_host, port=app_port, threaded=True, debug=True)
