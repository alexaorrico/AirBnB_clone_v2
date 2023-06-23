#!/usr/bin/python3
"""Start a Flask application."""

from models import storage
from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_context(self):
    """Close current session."""
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, threaded=True)
